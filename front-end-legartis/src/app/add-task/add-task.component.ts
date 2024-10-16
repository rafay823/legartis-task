import { Component, EventEmitter, Output } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { TaskService } from '../task.service';

@Component({
  selector: 'app-add-task',
  templateUrl: './add-task.component.html',
  styleUrls: ['./add-task.component.css'] 
})
export class AddTaskComponent {
  @Output() taskAdded = new EventEmitter<any>();

  constructor(private _dialog: MatDialog, private taskService: TaskService) {}

  closeAddTask() {
    this._dialog.closeAll();
  }

  saveTask(form: any) {
    if (form.valid) {
      const task = {
        title: form.value.title,
        description: form.value.description,
        deadline_date: form.value.date,
      };

      this.taskService.saveTask(task)
        .then(response => {
          console.log('Task saved successfully', response);
          this.taskAdded.emit(response);  // Emit the task to parent
          this.closeAddTask();
        })
        .catch(error => {
          console.error('Error saving task', error);
        });
    } else {
      console.log('Form is invalid');
    }
  }
}
