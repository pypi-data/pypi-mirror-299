import asyncio
import os
import random
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
from ape.common.evaluate.evaluate import Evaluate
from ape.common.generate.generate import Generate
from ape.common.generate.generate_base import BaseGenerate
from ape.common.metric.metric_base import BaseMetric
from ape.common.prompt import Prompt
from ape.common.types import DatasetItem
from ape.common.types.response_format import ResponseFormat
from ape.common.utils import logger

from ape.core.optimizer.sampled_fewshot import SampledFewshot
from ape.core.optimizer.bootstrap_fewshot import BootstrapFewShot
from ape.core.proposer.utils import extract_prompt
from ape.core.core_prompts import ApeCorePrompts


_nest_asyncio_applied = False


async def reformat_prompt(prompt: Prompt, response_format: ResponseFormat) -> Prompt:
    """Reformat the prompt to be in XML style."""
    formatter_filename: str
    match response_format["type"]:
        case "json_object":
            formatter_filename = "reformat-prompt-json-object"
        case "json_schema":
            formatter_filename = "reformat-prompt-json-schema"
    formatter = ApeCorePrompts.get(formatter_filename)
    new_prompt: Prompt
    retry_count = 0
    logger.info(f"Reformatting prompt: {prompt.dump()}")
    while True:
        try:
            res = await formatter(prompt=prompt.dump())
            extracted = extract_prompt(res)
            if response_format["type"] == "json_object":
                if "json" not in extracted.lower():
                    raise ValueError("Reformatted prompt does not include the word 'JSON'")
            logger.info(f"Reformatted prompt: {extracted}")
            new_prompt = Prompt.load(extracted)
            new_prompt.name = prompt.name
            new_prompt.response_format = response_format
            break
        except Exception as e:
            logger.error(f"Error reformatting prompt: {e}. Retrying...")
            retry_count += 1
            if retry_count > 10:
                logger.error("Failed to reformat prompt after 3 retries")
                logger.error("Generated prompt:" + res)
                raise e

    # new_prompt.fewshot_config = prompt.fewshot_config # TODO: fix this more pretty way
    return new_prompt


def is_notebook():
    try:
        from IPython import get_ipython

        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter
    except ImportError:
        return False  # IPython not installed


def run_async(coroutine):
    global _nest_asyncio_applied

    if not _nest_asyncio_applied:
        try:
            import nest_asyncio

            nest_asyncio.apply()
            _nest_asyncio_applied = True
        except ImportError:
            print("Please install nest_asyncio: !pip install nest_asyncio")
            raise

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If the loop is already running, create a new task and wait for it to complete
            task = asyncio.ensure_future(coroutine)
            return loop.run_until_complete(task)
        else:
            # If the loop is not running, use run_until_complete directly
            return loop.run_until_complete(coroutine)
    except RuntimeError:
        # If no event loop is present, use asyncio.run
        return asyncio.run(coroutine)


async def create_single_fewshot_demo_set(
    student: Prompt,
    trainset: List[DatasetItem],
    seed: int,
    max_labeled_demos: int,
    max_bootstrapped_demos: int,
    metric: BaseMetric,
    teacher_settings: dict,
    max_rounds: int,
    labeled_sample: bool,
    min_num_samples: int,
    metric_threshold: Any,
    teacher: Any,
    include_non_bootstrapped: bool,
    generate: BaseGenerate = Generate(),
) -> Prompt:
    trainset2 = list(trainset)

    if seed == -3 and include_non_bootstrapped:
        # zero-shot
        prompt2 = student.reset_copy()
    elif seed == -2 and max_labeled_demos > 0 and include_non_bootstrapped:
        # labels only
        optimizer = SampledFewshot(k=max_labeled_demos)
        prompt2 = await optimizer.optimize(student, trainset=trainset2, sample=labeled_sample)
    elif seed == -1:
        # unshuffled few-shot
        optimizer = BootstrapFewShot(
            generate=generate,
            metric=metric,
            max_bootstrapped_demos=max_bootstrapped_demos,
            max_labeled_demos=max_labeled_demos,
            teacher_settings=teacher_settings,
            max_rounds=max_rounds,
        )
        prompt2 = await optimizer.optimize(student, teacher=teacher, trainset=trainset2)
    else:
        # shuffled few-shot
        random.Random(seed).shuffle(trainset2)
        size = random.Random(seed).randint(min_num_samples, max_bootstrapped_demos)
        optimizer = BootstrapFewShot(
            generate=generate,
            metric=metric,
            metric_threshold=metric_threshold,
            max_bootstrapped_demos=size,
            max_labeled_demos=max_labeled_demos,
            teacher_settings=teacher_settings,
            max_rounds=max_rounds,
        )
        prompt2 = await optimizer.optimize(student, teacher=teacher, trainset=trainset2)

    return prompt2


async def create_n_fewshot_demo_sets(
    student: Prompt,
    num_candidate_sets: int,
    trainset: List[DatasetItem],
    max_labeled_demos: int,
    max_bootstrapped_demos: int,
    metric: BaseMetric,
    teacher_settings: dict,
    generate: BaseGenerate = Generate(),
    max_rounds=1,
    labeled_sample=True,
    min_num_samples=1,
    metric_threshold=None,
    teacher=None,
    include_non_bootstrapped=True,
    seed=0,
) -> List[List[DatasetItem]]:
    num_candidate_sets = max(num_candidate_sets, 3)
    random.Random(seed).shuffle(trainset)

    tasks = []
    for candidate_seed in range(-3, num_candidate_sets - 3):
        task = create_single_fewshot_demo_set(
            student=student,
            trainset=trainset,
            seed=candidate_seed,
            max_labeled_demos=max_labeled_demos,
            max_bootstrapped_demos=max_bootstrapped_demos,
            generate=generate,
            metric=metric,
            teacher_settings=teacher_settings,
            max_rounds=max_rounds,
            labeled_sample=labeled_sample,
            min_num_samples=min_num_samples,
            metric_threshold=metric_threshold,
            teacher=teacher,
            include_non_bootstrapped=include_non_bootstrapped,
        )
        tasks.append(task)

    max_workers = min(3, num_candidate_sets)
    semaphore = asyncio.Semaphore(max_workers)

    async def worker(task, i):
        async with semaphore:
            return await task

    fewshot_candidates = await asyncio.gather(*[worker(task, i) for i, task in enumerate(tasks)])

    return [
        prompt.fewshot for prompt in fewshot_candidates if prompt and hasattr(prompt, "fewshot")
    ]


def create_minibatch(trainset, batch_size=50):
    """Create a minibatch from the trainset."""

    # Ensure batch_size isn't larger than the size of the dataset
    batch_size = min(batch_size, len(trainset))

    # Randomly sample indices for the mini-batch
    sampled_indices = random.sample(range(len(trainset)), batch_size)

    # Create the mini-batch using the sampled indices
    minibatch = [trainset[i] for i in sampled_indices]

    return minibatch


async def eval_candidate_prompt(
    batch_size: int,
    trainset: List[DatasetItem],
    candidate_prompt: Prompt,
    evaluate: Evaluate,
):
    """Evaluate a candidate program on the trainset, using the specified batch size."""
    try:
        # Evaluate on the full trainset
        if batch_size >= len(trainset):
            score = await evaluate(candidate_prompt, testset=trainset, display_table=0)
        # Or evaluate on a minibatch
        else:
            score = await evaluate(
                candidate_prompt,
                testset=create_minibatch(trainset, batch_size),
                display_table=0,
            )
        if isinstance(score, tuple):
            score = score[0]

        return score
    except Exception as exc:
        logger.error(f"Error evaluating candidate prompt: {exc}")
        return 0


def save_candidate_prompt(prompt: Prompt, log_dir: Optional[str], trial_num: int, note=None):
    """Save the candidate prompt to the log directory."""

    if log_dir is None:
        return None

    # Ensure the directory exists
    eval_programs_dir = os.path.join(log_dir, "evaluated_prompts")
    os.makedirs(eval_programs_dir, exist_ok=True)

    # Define the save path for the program
    if note:
        save_path = os.path.join(eval_programs_dir, f"prompt_{trial_num}_{note}.prompt")
    else:
        save_path = os.path.join(eval_programs_dir, f"prompt_{trial_num}.prompt")

    # Save the prompt
    with open(save_path, "w") as f:
        f.write(prompt.dump())
    return save_path


def get_prompt_with_highest_avg_score(
    param_score_dict: Dict[str, List[Tuple[float, Prompt]]],
    fully_evaled_param_combos: Set[str],
) -> Tuple[Prompt, str]:
    """
    Returns the prompt with the highest average score from the batches evaluated so far.

    This function is used as a helper for Bayesian and minibatching optimizers.

    Args:
        param_score_dict: A dictionary mapping parameter combinations to lists of (score, prompt) tuples.
        fully_evaled_param_combos: A set of parameter combinations that have been fully evaluated.

    Returns:
        A tuple containing the best prompt and its corresponding parameter combination key.
    """
    results = [
        (key, np.mean([v[0] for v in values]), values[0][1])
        for key, values in param_score_dict.items()
    ]

    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

    for key, mean, prompt in sorted_results:
        if key not in fully_evaled_param_combos:
            logger.info(f"Best Combination: {key} with Mean = {mean:.4f}")
            return prompt, key

    # If all combinations are fully evaluated, return the overall best
    best_prompt, best_key = sorted_results[0][2], sorted_results[0][0]
    logger.warning("All parameter combinations fully evaluated. Returning overall best.")
    return best_prompt, best_key


async def find_best_fewshot(
    student: Prompt,
    num_candidate_sets: int,
    trainset: List[DatasetItem],
    max_labeled_demos: int,
    max_bootstrapped_demos: int,
    metric: BaseMetric,
    teacher_settings: dict,
    evaluate: Evaluate,
    max_rounds=1,
    labeled_sample=True,
    min_num_samples=1,
    metric_threshold=None,
    teacher=None,
    include_non_bootstrapped=True,
    batch_size=25,
    seed=0,
) -> Tuple[List[DatasetItem], float]:
    # Generate candidate few-shot sets
    fewshot_candidates = await create_n_fewshot_demo_sets(
        student=student,
        num_candidate_sets=num_candidate_sets,
        trainset=trainset,
        max_labeled_demos=max_labeled_demos,
        max_bootstrapped_demos=max_bootstrapped_demos,
        metric=metric,
        teacher_settings=teacher_settings,
        max_rounds=max_rounds,
        labeled_sample=labeled_sample,
        min_num_samples=min_num_samples,
        metric_threshold=metric_threshold,
        teacher=teacher,
        include_non_bootstrapped=include_non_bootstrapped,
        seed=seed,
    )

    async def evaluate_candidate(fewshot, semaphore):
        async with semaphore:
            candidate_prompt = student.deepcopy()
            candidate_prompt.fewshot = fewshot
            score = await eval_candidate_prompt(
                batch_size=min(batch_size, len(trainset)),  # Evaluate on minibatch
                trainset=trainset,
                candidate_prompt=candidate_prompt,
                evaluate=evaluate,
            )
            return (score, candidate_prompt, fewshot)

    max_concurrent = 5
    semaphore = asyncio.Semaphore(max_concurrent)

    results = await asyncio.gather(
        *[evaluate_candidate(fewshot, semaphore) for fewshot in fewshot_candidates]
    )

    best_score, best_prompt, best_fewshot = max(results, key=lambda x: x[0])

    return best_fewshot, best_score


# Example usage:
# best_prompt, best_score = await find_best_fewshot(
#     student=student_prompt,
#     num_candidate_sets=5,
#     trainset=trainset,
#     max_labeled_demos=3,
#     max_bootstrapped_demos=5,
#     metric=some_metric,
#     teacher_settings=teacher_settings,
#     evaluate=evaluate_function,
#     teacher=teacher_model
# )
# print(f"Best few-shot prompt score: {best_score}")
# print(f"Best few-shot prompt: {best_prompt.dump()}")
