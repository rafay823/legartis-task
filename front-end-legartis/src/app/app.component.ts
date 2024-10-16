import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { AddTaskComponent } from './add-task/add-task.component';
import { TaskService } from './task.service';
import { environment } from '../environment'; 
import { Observable } from 'rxjs'; 

interface Task {
  title: string;
  description: string;
  deadline_date: Date;
  task_status: boolean;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']  
})
export class AppComponent implements OnInit {
  title = 'project';
  tasks: Task[] = [];
  searchTerm: string = '';

  constructor(private _dialog: MatDialog, private http: HttpClient, private taskService: TaskService) {}

  ngOnInit() {
    this.fetchTasks();
  }

  openAddTaskDialogForm() {
    console.log('Add Task dialog opened');

    const dialogRef = this._dialog.open(AddTaskComponent);

    dialogRef.componentInstance.taskAdded.subscribe((newTask: Task) => {
      this.tasks.push({
        ...newTask,
        deadline_date: new Date(newTask.deadline_date)
      });
      console.log('New task added to the list:', newTask);
    });
  }

  onTaskStatusChange(task: any) {
    console.log('Task status changed:', task);
    this.taskService.updateTaskStatus(task, task.id)
      .then((response: Task) => {
        console.log('Task status updated:', response);
      })
      .catch((error) => {
        console.error('Error updating task status:', error);
      });
  }

  fetchTasks() {
    const baseUrl = environment.baseApiUrl; 

    this.http.get<Task[]>(`${baseUrl}/tasks`).subscribe({
      next: (data) => {
        this.tasks = data.map(task => ({
          ...task,
          deadline_date: new Date(task.deadline_date) // Convert to Date object
        }));
      },
      error: (error) => {
        console.error('Error fetching tasks:', error);
      },
      complete: () => {
        console.log('Task fetching complete.');
      }
    });
  }

  filteredTasks(): Task[] {
    if (!this.searchTerm) {
      return this.tasks;
    }

    return this.tasks.filter(task =>
      task.title.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      task.description.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
}
