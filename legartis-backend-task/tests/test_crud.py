import pytest
from unittest.mock import AsyncMock, MagicMock, ANY
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.crud import create_task

@pytest.mark.asyncio
async def test_create_task_success():
    mock_db = AsyncMock()
    task_title = "Sample Task"
    task_description = "This is a test task"
    task_deadline = datetime.now()
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    result = await create_task(mock_db, task_title, task_description, task_deadline)
    mock_db.add.assert_called_once_with(ANY)
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(ANY)
    assert result.title == task_title
    assert result.description == task_description
    assert result.deadline_date == task_deadline
    assert result.task_status is False


@pytest.mark.asyncio
async def test_create_task_integrity_error():
    mock_db = AsyncMock()
    task_title = "Sample Task"
    task_description = "This is a test task"
    task_deadline = datetime.now()
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock(side_effect=IntegrityError(None, None, None))
    mock_db.rollback = AsyncMock()
    with pytest.raises(ValueError, match="Task could not be created due to integrity error."):
        await create_task(mock_db, task_title, task_description, task_deadline)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.rollback.assert_awaited_once()
