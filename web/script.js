const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');
const gameCanvas = document.getElementById('gameCanvas');
const ctx = gameCanvas.getContext('2d');
const scoreElement = document.getElementById('score');
const statusElement = document.getElementById('status');
const cursorElement = document.getElementById('hand-cursor');
const landingScreen = document.getElementById('landing-screen');
const startButton = document.getElementById('start-btn');
const restartButton = document.getElementById('restart-btn');
const gameOverScreen = document.getElementById('game-over-screen');
const finalScoreElement = document.getElementById('final-score');
const scanScreen = document.getElementById('scan-screen');
const scanStatus = document.getElementById('scan-status');

// --- Game Logic ---

const ROWS = 20;
const COLS = 10;
const BLOCK_SIZE = 30;
// Neon Colors
const NEON_COLORS = [
    '#00f3ff', // Cyan
    '#ff00ff', // Pink
    '#00ff41', // Green
    '#ffd700', // Gold
    '#ff1a1a', // Red
    '#bd00ff', // Purple
    '#ff9100'  // Orange
];
const SHAPES = [
    [[1, 1, 1, 1]], // I
    [[1, 1], [1, 1]], // O
    [[1, 1, 0], [0, 1, 1]], // Z
    [[0, 1, 1], [1, 1, 0]], // S
    [[1, 1, 1], [0, 1, 0]], // T
    [[1, 1, 1], [1, 0, 0]], // L
    [[1, 1, 1], [0, 0, 1]]  // J
];

let grid = Array.from({ length: ROWS }, () => Array(COLS).fill(null));
let score = 0;
let gameOver = false;
let gameRunning = false;

class Block {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.shape = SHAPES[Math.floor(Math.random() * SHAPES.length)];
        this.color = NEON_COLORS[Math.floor(Math.random() * NEON_COLORS.length)];
    }

    rotate() {
        this.shape = this.shape[0].map((_, i) => this.shape.map(row => row[i]).reverse());
    }
}

let currentBlock = new Block(3, 0);

function drawNeonRect(ctx, x, y, size, color) {
    ctx.shadowBlur = 15;
    ctx.shadowColor = color;
    ctx.fillStyle = color;
    ctx.fillRect(x, y, size, size);

    // Inner light
    ctx.shadowBlur = 0;
    ctx.fillStyle = 'rgba(255,255,255,0.3)';
    ctx.fillRect(x + 5, y + 5, size - 10, size - 10);

    // Border
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1;
    ctx.strokeRect(x, y, size, size);
}

function drawGrid() {
    ctx.clearRect(0, 0, gameCanvas.width, gameCanvas.height);

    // Subtle Grid Lines
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let i = 0; i <= COLS; i++) {
        ctx.moveTo(i * BLOCK_SIZE, 0);
        ctx.lineTo(i * BLOCK_SIZE, ROWS * BLOCK_SIZE);
    }
    for (let i = 0; i <= ROWS; i++) {
        ctx.moveTo(0, i * BLOCK_SIZE);
        ctx.lineTo(COLS * BLOCK_SIZE, i * BLOCK_SIZE);
    }
    ctx.stroke();

    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            if (grid[r][c]) {
                drawNeonRect(ctx, c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, grid[r][c]);
            }
        }
    }
}

function drawBlock(block) {
    block.shape.forEach((row, r) => {
        row.forEach((cell, c) => {
            if (cell) {
                drawNeonRect(ctx, (block.x + c) * BLOCK_SIZE, (block.y + r) * BLOCK_SIZE, BLOCK_SIZE, block.color);
            }
        });
    });
}

function checkCollision(offsetX = 0, offsetY = 0, shape = currentBlock.shape) {
    for (let r = 0; r < shape.length; r++) {
        for (let c = 0; c < shape[r].length; c++) {
            if (shape[r][c]) {
                let newX = currentBlock.x + c + offsetX;
                let newY = currentBlock.y + r + offsetY;
                if (newX < 0 || newX >= COLS || newY >= ROWS) return true;
                if (newY >= 0 && grid[newY][newX]) return true;
            }
        }
    }
    return false;
}

function lockBlock() {
    let pushedTop = false;
    currentBlock.shape.forEach((row, r) => {
        row.forEach((cell, c) => {
            if (cell) {
                let newY = currentBlock.y + r;
                let newX = currentBlock.x + c;
                if (newY >= 0 && newY < ROWS && newX >= 0 && newX < COLS) {
                    grid[newY][newX] = currentBlock.color;
                    if (newY === 0) {
                        pushedTop = true;
                    }
                }
            }
        });
    });

    if (pushedTop) {
        gameOver = true;
        showGameOver();
        return;
    }

    clearLines();
    currentBlock = new Block(3, 0);
    if (checkCollision()) {
        gameOver = true;
        showGameOver();
    }
}

function clearLines() {
    let linesCleared = 0;
    for (let r = ROWS - 1; r >= 0; r--) {
        if (grid[r].every(cell => cell !== null)) {
            grid.splice(r, 1);
            grid.unshift(Array(COLS).fill(null));
            linesCleared++;
            r++; // Check same row again
        }
    }
    if (linesCleared > 0) {
        score += linesCleared * 100 * linesCleared; // Bonus for multi-line
        scoreElement.innerText = score.toString().padStart(6, '0');
    }
}

function moveBlock(dx, dy) {
    if (!gameOver && gameRunning) {
        if (!checkCollision(dx, dy)) {
            currentBlock.x += dx;
            currentBlock.y += dy;
        } else if (dy > 0) {
            lockBlock();
        }
    }
}

function rotateBlock() {
    if (!gameOver && gameRunning) {
        const originalShape = currentBlock.shape;
        currentBlock.rotate();
        if (checkCollision()) {
            currentBlock.shape = originalShape;
        }
    }
}

// Game Loop
let lastTime = 0;
let dropCounter = 0;
let dropInterval = 500;

function update(time = 0) {
    const deltaTime = time - lastTime;
    lastTime = time;

    if (gameRunning && !gameOver) {
        dropCounter += deltaTime;
        if (dropCounter > dropInterval) {
            moveBlock(0, 1);
            dropCounter = 0;
        }
    }

    drawGrid();
    if (gameRunning && !gameOver) {
        drawBlock(currentBlock);
    }

    requestAnimationFrame(update);
}

// --- Hand Tracking Logic (Virtual Joystick) ---

let lastMoveTime = 0;
const MOVE_DELAY_INITIAL = 150;
let currentMoveDelay = MOVE_DELAY_INITIAL;
let lastRotateTime = 0;
const ROTATE_DELAY = 500;
let isScanning = false;
let scanTimer = null;

function onResults(results) {
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        // Hand Detected
        const landmarks = results.multiHandLandmarks[0];

        drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, { color: '#00f3ff', lineWidth: 2 });
        drawLandmarks(canvasCtx, landmarks, { color: '#ff00ff', lineWidth: 1 });

        // HAND SCAN LOGIC
        if (isScanning && !gameRunning && !gameOver) {
            if (!scanTimer) {
                scanStatus.innerText = "HAND DETECTED! STARTING IN 2...";
                scanStatus.style.color = "var(--neon-green)";
                scanTimer = setTimeout(() => {
                    scanStatus.innerText = "STARTING IN 1...";
                    setTimeout(() => {
                        isScanning = false;
                        scanScreen.classList.add('hidden');
                        gameRunning = true;
                        update();
                        statusElement.innerText = "SYSTEM ACTIVE";
                    }, 1000);
                }, 1000);
            }
        }

        // GAME CONTROL LOGIC
        if (gameRunning) {
            let handX = landmarks[9].x;
            let cursorPercent = (1 - handX) * 100;
            cursorElement.style.left = `${cursorPercent}%`;

            const currentTime = Date.now();

            if (cursorPercent < 40) {
                currentMoveDelay = cursorPercent < 20 ? 100 : 200;
                if (currentTime - lastMoveTime > currentMoveDelay) {
                    moveBlock(-1, 0);
                    lastMoveTime = currentTime;
                    statusElement.innerText = "MOVING LEFT";
                }
            } else if (cursorPercent > 60) {
                currentMoveDelay = cursorPercent > 80 ? 100 : 200;
                if (currentTime - lastMoveTime > currentMoveDelay) {
                    moveBlock(1, 0);
                    lastMoveTime = currentTime;
                    statusElement.innerText = "MOVING RIGHT";
                }
            } else {
                statusElement.innerText = "HOLDING";
            }

            const indexTip = landmarks[8];
            const thumbTip = landmarks[4];
            const dx = indexTip.x - thumbTip.x;
            const dy = indexTip.y - thumbTip.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 0.05) {
                if (currentTime - lastRotateTime > ROTATE_DELAY) {
                    rotateBlock();
                    lastRotateTime = currentTime;
                    statusElement.innerText = "ROTATING";
                    statusElement.style.color = "#ff00ff";
                    setTimeout(() => statusElement.style.color = "#ffd700", 200);
                }
            }
        }
    } else {
        // No Hand
        if (isScanning && scanTimer) {
            clearTimeout(scanTimer);
            scanTimer = null;
            scanStatus.innerText = "PLEASE SHOW HAND TO CAMERA";
            scanStatus.style.color = "white";
        }
    }

    canvasCtx.restore();
}

const hands = new Hands({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
    }
});

hands.setOptions({
    maxNumHands: 1,
    modelComplexity: 1,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});
hands.onResults(onResults);

// Initialization
const camera = new Camera(videoElement, {
    onFrame: async () => {
        await hands.send({ image: videoElement });
    },
    width: 640,
    height: 480
});

// Event Listeners
startButton.addEventListener('click', () => {
    landingScreen.classList.add('hidden');
    scanScreen.classList.remove('hidden');
    isScanning = true;
    camera.start();
});

restartButton.addEventListener('click', () => {
    resetGame();
});

function showGameOver() {
    gameRunning = false;
    finalScoreElement.innerText = score.toString().padStart(6, '0');
    statusElement.innerText = "TERMINATED";
    gameOverScreen.classList.remove('hidden');
    gameOverScreen.style.opacity = "1";
    gameOverScreen.style.pointerEvents = "all";
}

function resetGame() {
    grid = Array.from({ length: ROWS }, () => Array(COLS).fill(null));
    score = 0;
    scoreElement.innerText = "000000";
    statusElement.innerText = "SYSTEM ACTIVE";
    statusElement.style.color = "var(--neon-gold)";
    currentBlock = new Block(3, 0);
    gameOver = false;
    gameRunning = true;

    gameOverScreen.classList.add('hidden');
    gameOverScreen.style.opacity = "0";
    gameOverScreen.style.pointerEvents = "none";
}

// --- 3D Tilt Effect for Landing Page ---
// --- 3D Tilt Effect for Landing & Game Over Pages ---
document.addEventListener('mousemove', (e) => {
    // Check if Landing or Game Over is active
    let activeContent = null;

    if (!landingScreen.classList.contains('hidden')) {
        activeContent = landingScreen.querySelector('.landing-content');
    } else if (!gameOverScreen.classList.contains('hidden')) {
        activeContent = gameOverScreen.querySelector('.landing-content');
    }

    if (!activeContent) return;

    const x = (window.innerWidth / 2 - e.pageX) / 25;
    const y = (window.innerHeight / 2 - e.pageY) / 25;

    activeContent.style.transform = `rotateY(${x}deg) rotateX(${y}deg)`;
});
