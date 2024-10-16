import { Injectable } from '@angular/core';
import axios from 'axios';
import { environment } from '../environment'; 

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  
  async saveTask(task: { title: string; description: string; deadline_date: string }): Promise<any> {
    const baseUrl = environment.baseApiUrl; 
    console.log(`Posting to URL: ${baseUrl}`);  
    try {
      const response = await axios.post(`${baseUrl}/task`, task);
      return response.data; 
    } catch (error) {
      console.error("Error saving task:", error);
      throw error;  
    }
  }

  async updateTaskStatus(
    task: { task_status: boolean; title: string; description: string; deadline_date: string },
    id: number
  ): Promise<any> {
    const baseUrl = environment.baseApiUrl;
  
    try {
      const response = await axios.put(`${baseUrl}/tasks/${id}`, {
        task_status: task.task_status,
        title: task.title,
        description: task.description,
        deadline_date: task.deadline_date
      });
      return response.data;
    } catch (error) {
      console.error("Error updating task status:", error);
      throw error; 
    }
  }

}
