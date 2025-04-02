document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const studyForm = document.getElementById('study-form');
    const submitBtn = document.getElementById('submit-btn');
    const loadingSection = document.getElementById('loading');
    const resultsSection = document.getElementById('results');
    const researchContent = document.getElementById('research-content');
    const flashcardsContainer = document.getElementById('flashcards-container');
    const studyGuideContent = document.getElementById('study-guide-content');
    
    // Track user progress
    let totalFlashcards = 0;
    let viewedFlashcards = 0;
    
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to current tab
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(`${tabId}-tab`).classList.add('active');
            
            // Add subtle animation to tab content
            const activePane = document.getElementById(`${tabId}-tab`);
            activePane.style.opacity = '0';
            setTimeout(() => {
                activePane.style.opacity = '1';
            }, 50);
        });
    });
    
    // Form submission
    studyForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const topic = document.getElementById('topic').value.trim();
        
        if (!topic) {
            showNotification('Please enter a study topic', 'error');
            return;
        }
        
        // Show loading state
        submitBtn.disabled = true;
        loadingSection.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        
        // Smooth scroll to loading section
        loadingSection.scrollIntoView({ behavior: 'smooth' });
        
        // Animate progress bar
        const progressBar = document.querySelector('.progress-fill');
        
        // Reset progress bar
        progressBar.style.width = '5%';
        
        // Gradually increase progress
        let progress = 5;
        
        // Start progress animation
        const progressInterval = setInterval(() => {
            if (progress < 85) {
                progress += Math.random() * 8;
                progressBar.style.width = `${progress}%`;
            }
        }, 800);
        
        try {
            // Make API request
            const response = await fetch('/api/study', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ topic })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Complete the progress bar animation
            progressBar.style.width = '100%';
            
            // Clear the interval
            clearInterval(progressInterval);
            
            // Wait a moment for visual completion before showing results
            setTimeout(() => {
                // Process and display the data
                displayResults(data);
            }, 500);
        } catch (error) {
            // Clear the interval on error
            clearInterval(progressInterval);
            
            console.error('Error:', error);
            showNotification('An error occurred while processing your request', 'error');
            submitBtn.disabled = false;
            loadingSection.classList.add('hidden');
        }
    });
    
    // Display results function
    function displayResults(data) {
        // Reset progress trackers for flashcards
        totalFlashcards = 0;
        viewedFlashcards = 0;
        
        // Display research content
        researchContent.innerHTML = data.research ? formatText(data.research) : '<p>No research data available.</p>';
        
        // Display flashcards
        flashcardsContainer.innerHTML = '';
        if (data.flashcards) {
            if (Array.isArray(data.flashcards)) {
                // If flashcards is an array of objects
                data.flashcards.forEach((card, index) => {
                    // Stagger flashcard creation for a nicer visual effect
                    setTimeout(() => {
                        createFlashcard(card.question, card.answer);
                    }, index * 150);
                });
            } else {
                // If flashcards is a string
                flashcardsContainer.innerHTML = formatText(data.flashcards);
            }
        } else {
            flashcardsContainer.innerHTML = '<p>No flashcard data available.</p>';
        }
        
        // Display study guide
        studyGuideContent.innerHTML = data.study_guide ? formatText(data.study_guide) : '<p>No study guide available.</p>';
        
        // Hide loading, show results
        loadingSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');
        
        // Smooth scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        // Re-enable the submit button
        submitBtn.disabled = false;
        
        // Show success notification 
        showNotification('Your study materials have been generated!', 'success');
    }
    
    // Format text with markdown-like formatting
    function formatText(text) {
        if (!text) return '';
        
        // Create a temporary div to work with
        let div = document.createElement('div');
        
        // Process code blocks first (prevent internal content from being processed)
        text = text.replace(/```(?:(\w+)\n)?([\s\S]*?)```/g, function(match, lang, code) {
            return `<pre><code class="language-${lang || ''}">${code.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code></pre>`;
        });
        
        // Process inline code
        text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Replace headings with appropriate HTML tags
        text = text.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
        text = text.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
        text = text.replace(/^# (.*?)$/gm, '<h1>$1</h1>');
        text = text.replace(/^#### (.*?)$/gm, '<h4>$1</h4>');
        text = text.replace(/^##### (.*?)$/gm, '<h5>$1</h5>');
        text = text.replace(/^###### (.*?)$/gm, '<h6>$1</h6>');
        
        // Process horizontal rules
        text = text.replace(/^\-\-\-+$/gm, '<hr>');
        
        // Replace bold and italic
        text = text.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Process unordered lists
        text = text.replace(/^\s*[\-\*] (.*?)$/gm, '<li>$1</li>');
        text = text.replace(/(<li>.*?<\/li>\n?)+/g, '<ul>$&</ul>');
        
        // Process ordered lists
        text = text.replace(/^\s*(\d+)\. (.*?)$/gm, '<li>$2</li>');
        
        // Process blockquotes
        text = text.replace(/^> (.*?)$/gm, '<blockquote>$1</blockquote>');
        
        // Process links
        text = text.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
        
        // Replace paragraphs (lines followed by blank lines)
        text = text.replace(/^(?!<[a-z]*>)(.*?)$/gm, function(match) {
            if (match.trim() === '') return '';
            return '<p>' + match + '</p>';
        });
        
        // Fix nested paragraphs inside list items
        text = text.replace(/<li><p>(.*?)<\/p><\/li>/g, '<li>$1</li>');
        
        // Replace line breaks for remaining content
        text = text.replace(/\n\n+/g, '</p><p>');
        text = text.replace(/<p><\/p>/g, '');
        
        // Final clean-up by setting HTML and returning it
        div.innerHTML = text;
        return div.innerHTML;
    }
    
    // Create flashcard element
    function createFlashcard(question, answer) {
        const flashcard = document.createElement('div');
        flashcard.className = 'flashcard';
        
        flashcard.innerHTML = `
            <div class="flashcard-inner">
                <div class="flashcard-front">
                    <h4>${question}</h4>
                </div>
                <div class="flashcard-back">
                    <p>${answer}</p>
                </div>
            </div>
        `;
        
        flashcard.addEventListener('click', function() {
            const wasFlipped = this.classList.contains('flipped');
            this.classList.toggle('flipped');
            
            // If card is being flipped to the back (answer) side for the first time
            if (!wasFlipped) {
                viewedFlashcards++;
                
                // If all flashcards have been viewed, show a notification
                if (viewedFlashcards === totalFlashcards) {
                    setTimeout(() => {
                        showNotification('Great job! You\'ve reviewed all flashcards!', 'success');
                    }, 500);
                }
            }
        });
        
        // Track total number of flashcards
        totalFlashcards++;
        
        // Add with animation
        flashcard.style.opacity = '0';
        flashcard.style.transform = 'translateY(20px)';
        flashcardsContainer.appendChild(flashcard);
        
        // Trigger animation after a small delay
        setTimeout(() => {
            flashcard.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            flashcard.style.opacity = '1';
            flashcard.style.transform = 'translateY(0)';
        }, 50);
    }
    
    // Notification system
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        // Set icon based on type
        let icon = 'info-circle';
        if (type === 'success') icon = 'check-circle';
        if (type === 'error') icon = 'exclamation-circle';
        if (type === 'warning') icon = 'exclamation-triangle';
        
        notification.innerHTML = `
            <i class="fas fa-${icon}"></i>
            <span>${message}</span>
        `;
        
        // Add to DOM
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Remove after delay
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    }
});