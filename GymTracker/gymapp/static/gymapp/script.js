// Timer functionality

let timerInterval;
let timeRemaining = 0;
let isRunning = false;
let originalTime = 0;

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function updateDisplay() {
    const display = document.getElementById('timerDisplay');
    if (display) {
        display.textContent = formatTime(timeRemaining);
    }
}

function updateTimerProgress() {
    const timerCircle = document.querySelector('.timer-circle');
    if (timerCircle && originalTime > 0) {
        const progress = ((originalTime - timeRemaining) / originalTime) * 100;
        
    }
}

function startTimer() {
    if (timeRemaining <= 0) {
        showTimerAlert('⚠️ Please set a timer first!', 'warning');
        return;
    }
    
    isRunning = true;
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const timerCircle = document.querySelector('.timer-circle');
    
    
    if (startBtn) startBtn.style.display = 'none';
    if (pauseBtn) pauseBtn.style.display = 'inline-flex';
    
    
    if (timerCircle) {
        timerCircle.classList.add('running');
        timerCircle.classList.remove('finished');
    }
    
    
    if (originalTime === 0) {
        originalTime = timeRemaining;
    }
    
    timerInterval = setInterval(() => {
        timeRemaining--;
        updateDisplay();
        
        
        if (timeRemaining === 10) {
            showTimerAlert('⏰ 10 seconds remaining!', 'warning');
        }
        
        if (timeRemaining <= 0) {
            finishTimer();
        }
    }, 1000);
}

function pauseTimer() {
    clearInterval(timerInterval);
    isRunning = false;
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const timerCircle = document.querySelector('.timer-circle');
    
    
    if (startBtn) startBtn.style.display = 'inline-flex';
    if (pauseBtn) pauseBtn.style.display = 'none';
    
    
    if (timerCircle) {
        timerCircle.classList.remove('running');
    }
    
    showTimerAlert('⏸️ Timer paused', 'info');
}

function stopTimer() {
    clearInterval(timerInterval);
    isRunning = false;
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const timerCircle = document.querySelector('.timer-circle');
    
    
    if (startBtn) startBtn.style.display = 'inline-flex';
    if (pauseBtn) pauseBtn.style.display = 'none';
    
    
    if (timerCircle) {
        timerCircle.classList.remove('running', 'finished');
    }
    
    showTimerAlert('⏹️ Timer stopped', 'info');
}

function resetTimer() {
    stopTimer();
    timeRemaining = 0;
    originalTime = 0;
    updateDisplay();
    
    const timerCircle = document.querySelector('.timer-circle');
    if (timerCircle) {
        timerCircle.classList.remove('running', 'finished');
    }
    
    showTimerAlert('🔄 Timer reset', 'info');
}

function finishTimer() {
    clearInterval(timerInterval);
    isRunning = false;
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const timerCircle = document.querySelector('.timer-circle');
    
    
    if (startBtn) startBtn.style.display = 'inline-flex';
    if (pauseBtn) pauseBtn.style.display = 'none';
    
    
    if (timerCircle) {
        timerCircle.classList.remove('running');
        timerCircle.classList.add('finished');
        
        
        setTimeout(() => {
            timerCircle.classList.remove('finished');
        }, 1000);
    }
    
    
    originalTime = 0;
    
    
    showTimerAlert('🎉 Timer finished! Great workout!', 'success');
    
    
    playNotificationSound();
    
    
    if (navigator.vibrate) {
        navigator.vibrate([200, 100, 200]);
    }
}

function setTimer(seconds) {
    
    if (isRunning) {
        stopTimer();
    }
    
    timeRemaining = seconds;
    originalTime = 0; 
    updateDisplay();
    
    
    const timerCircle = document.querySelector('.timer-circle');
    if (timerCircle) {
        timerCircle.style.transform = 'scale(1.05)';
        setTimeout(() => {
            timerCircle.style.transform = 'scale(1)';
        }, 200);
    }
    
    showTimerAlert(`⏱️ Timer set to ${formatTime(seconds)}`, 'info');
}

function setCustomTimer() {
    const customInput = document.getElementById('customMinutes');
    if (customInput) {
        const minutes = parseInt(customInput.value);
        if (minutes && minutes > 0 && minutes <= 120) {
            setTimer(minutes * 60);
            customInput.value = '';
            
            
            customInput.style.borderColor = '#4cc9f0';
            setTimeout(() => {
                customInput.style.borderColor = '';
            }, 1000);
        } else {
            showTimerAlert('⚠️ Please enter a valid number (1-120 minutes)!', 'error');
            
            
            customInput.style.borderColor = '#f72585';
            customInput.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => {
                customInput.style.borderColor = '';
                customInput.style.animation = '';
            }, 1000);
        }
    }
}


function showTimerAlert(message, type = 'info') {
    
    const existingAlerts = document.querySelectorAll('.timer-alert');
    existingAlerts.forEach(alert => alert.remove());
    
    
    const alert = document.createElement('div');
    alert.className = `timer-alert timer-alert-${type}`;
    alert.textContent = message;
    
    
    alert.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
        max-width: 300px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    `;
    
    
    switch(type) {
        case 'success':
            alert.style.background = 'linear-gradient(45deg, #4cc9f0, #4361ee)';
            break;
        case 'warning':
            alert.style.background = 'linear-gradient(45deg, #f72585, #b5179e)';
            break;
        case 'error':
            alert.style.background = 'linear-gradient(45deg, #b5179e, #7209b7)';
            break;
        default:
            alert.style.background = 'linear-gradient(45deg, #4361ee, #7209b7)';
    }
    
    document.body.appendChild(alert);
    
    
    setTimeout(() => {
        alert.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => alert.remove(), 300);
    }, 3000);
}


function playNotificationSound() {
    try {
        
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
    } catch (error) {
        
        console.log('Audio notification not available');
    }
}


function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    const themeBtn = document.querySelector('.theme-toggle');
    if (themeBtn) {
        themeBtn.textContent = document.body.classList.contains('dark-theme') ? '☀️' : '🌙';
    }
    localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
}


document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        const themeBtn = document.querySelector('.theme-toggle');
        if (themeBtn) themeBtn.textContent = '☀️';
    }
    
    updateDisplay();
    
    
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            alert.style.animation = 'slideOut 0.5s ease-in-out forwards';
            setTimeout(() => alert.remove(), 500);
        });
    }, 3000);
});

const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);