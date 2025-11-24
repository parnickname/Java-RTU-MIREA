package domain.model;

public class Task {

    private final Long id;
    private final String title;
    private final boolean completed;

    public Task(Long id, String title, boolean completed) {
        this.id = id;
        this.title = title;
        this.completed = completed;
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public boolean isCompleted() {
        return completed;
    }

    public Task complete() {
        return completed ? this : new Task(this.id, this.title, true);
    }

    public Task withTitle(String newTitle) {
        return new Task(this.id, newTitle, this.completed);
    }

    // Создание нового таска с обновлённым completed
    public Task withCompleted(boolean newCompleted) {
        return new Task(this.id, this.title, newCompleted);
    }
}
