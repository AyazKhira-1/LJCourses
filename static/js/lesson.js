document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('lesson-video');
    const markCompleteBtn = document.getElementById('markCompleteBtn');
    const lessonId = document.body.dataset.lessonId;

    if (!lessonId) {
        console.error('Lesson ID not found');
        return;
    }

    // Function to mark lesson as complete
    async function markLessonComplete() {
        try {
            const response = await fetch(`/api/complete-lesson/${lessonId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.success) {
                // Update button UI
                if (markCompleteBtn) {
                    markCompleteBtn.innerHTML = `
                        <span class="material-icons" style="font-size: 1.25rem;">check_circle</span>
                        <span>Completed</span>
                    `;
                    markCompleteBtn.classList.remove('btn-outline-secondary');
                    markCompleteBtn.classList.add('btn-success', 'text-white');
                    markCompleteBtn.disabled = true;
                }

                // If video ended and there is a next lesson, redirect
                if (video && video.ended && data.next_lesson_url) {
                    window.location.href = data.next_lesson_url;
                } else {
                    // Optionally reload to update sidebar/progress, or manually update DOM
                    // For now, let's reload to ensure all state (sidebar checkmarks, etc.) is consistent
                    // providing a better user experience than partial updates.
                    // However, if we just want to update the button, we can skip reload.
                    // But if the user clicked the button manually, they might want to stay on page.
                    // If video ended, we might want to go to next.

                    if (!video.ended) {
                        // If button click, reload to show updated progress in sidebar
                        window.location.reload();
                    }
                }

            } else {
                console.error('Failed to mark lesson complete:', data.error);
                alert('Failed to mark lesson as complete. Please try again.');
            }
        } catch (error) {
            console.error('Error marking lesson complete:', error);
            alert('An error occurred. Please check your internet connection.');
        }
    }

    // Event listener for video end
    if (video) {
        video.addEventListener('ended', () => {
            markLessonComplete();
        });
    }

    // Event listener for mark complete button action
    if (markCompleteBtn) {
        markCompleteBtn.addEventListener('click', () => {
            markLessonComplete();
        });
    }
});
