package application;

import domain.model.Task;
import domain.ports.TaskRepositoryPort;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TaskService {
    private final TaskRepositoryPort taskRepository;

    public TaskService(TaskRepositoryPort taskRepository) {
        this.taskRepository = taskRepository;
    }

    public List<Task> findAll() {
        return taskRepository.findAll();
    }

    public Task add(String title) {
        Task task = new Task(null, title, false);
        return taskRepository.save(task);
    }

    public Task complete(Long id) {
        Task existing = taskRepository.findById(id).orElseThrow(() -> new RuntimeException("Task with id " + id + " not found"));
        if (existing.isCompleted()) {
            throw new RuntimeException("Task with id " + id + " is already completed");
        } else {
            Task updated = existing.complete();
            taskRepository.save(updated);
            return updated;
        }
    }

    public void delete(Long id) {
        taskRepository.deleteById(id);
    }
}
