from loguru import logger
from handshake.services.DBService.models.dynamic_base import TaskBase, JobType
from uuid import uuid4, UUID
from typing import Union, List
from handshake.services.DBService.models.result_base import TestLogBase, LogType


async def register_patch_suite(suiteID: str, testID: str, connection=None) -> TaskBase:
    return await TaskBase.create(
        ticketID=suiteID, test_id=testID, type=JobType.MODIFY_SUITE, using_db=connection
    )


async def register_patch_test_run(testID: str, connection=None) -> TaskBase:
    _, created = await TaskBase.get_or_create(
        type=JobType.MODIFY_TEST_RUN,
        test_id=testID,
        ticketID=testID,
        using_db=connection,
    )
    return _


async def register_bulk_patch_suites(
    testID: str,
    suites: List[str],
    connection=None,
) -> List[TaskBase]:
    tasks = await TaskBase.bulk_create(
        [
            TaskBase(ticketID=suite, test_id=testID, type=JobType.MODIFY_SUITE)
            for suite in suites
        ],
        100,
        using_db=connection,
    )
    return tasks


async def mark_for_prune_task(test_id: str):
    # someone called this explicitly hence it's a warning

    logger.warning("Requested to prune some tasks")
    await TaskBase.create(
        ticketID=str(uuid4()), type=JobType.PRUNE_TASKS, test_id=test_id
    )


async def skip_test_run(test_id: Union[str, UUID], reason: str, **extra) -> False:
    logger.error(reason)
    await TestLogBase.create(
        test_id=str(test_id), message=reason, type=LogType.ERROR, feed=extra
    )
    await mark_for_prune_task(test_id)
    return False


async def warn_about_test_run(test_id: Union[str, UUID], about: str, **extra) -> True:
    logger.warning(about)
    await TestLogBase.create(
        test_id=str(test_id), message=about, type=LogType.WARN, feed=extra
    )
    return True
