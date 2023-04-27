const canvas = document.querySelector('canvas');
const context = canvas.getContext('2d');

let particleCount;
if (innerWidth >= innerHeight) {
	particleCount = parseInt(innerWidth / 20);
} else {
	particleCount = parseInt(innerHeight / 20);
}
let particleObjects = [];
let connectorObjects = [];
let mouseOver = false;
let mouseX;
let mouseY;
let selectedTheme = 0;
let colorThemes = [
	{
		circle: '#000000',
		line: '#000000',
		bg: '#ff124f',
		shadowColor: '#000000',
		pFont: '#000000',
	},
	{
		circle: '#2f404d',
		line: '#3d898d',
		bg: '#85ebd9',
		shadowColor: '#2f404d',
		pFont: '#2f404d',
	},
	{
		circle: '#ff2a6d',
		line: '#05d9e8',
		bg: '#000000',
		shadowColor: '#ff2a6d',
		pFont: '#ff2a6d',
	},
	{
		circle: '#9c9c9c',
		line: '#9c9c9c',
		bg: '#ffffff',
		shadowColor: '#9c9c9c',
		pFont: '#9c9c9c',
	},
	{
		circle: '#ffffff',
		line: '#ffffff',
		bg: '#000000',
		shadowColor: '#ffffff',
		pFont: '#ffffff',
	},
	{
		circle: '#fe00fe',
		line: '#ffffff',
		bg: '#120458',
		shadowColor: '#fe00fe',
		pFont: '#fe00fe',
	},
	{
		circle: '#65dc98',
		line: '#a0ffe3',
		bg: '#222035',
		shadowColor: '#65dc98',
		pFont: '#65dc98',
	},
	{
		circle: '#001eff',
		line: '#001eff',
		bg: '#d600ff',
		shadowColor: '#001eff',
		pFont: '#001eff',
	},
];
let autoChangeTheme = false;
let autoChangeThemeInterval;

const canvasInit = () => {
	colorSwitch(selectedTheme);

	canvas.width = window.innerWidth - 2;
	canvas.height = window.innerHeight - 2;

	for (let i = 0; i < particleCount; i++) {
		let newParticle = new Particle();
		newParticle.draw();
		particleObjects.push(newParticle);
	}

	window.requestAnimationFrame(mainLoop);
}

const getRandomNum = (min, max) => {
	return Math.random() * (max - min) + min;
}

const getRandomInt = (min, max) => {
	min = Math.ceil(min);
	max = Math.floor(max);
	return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}

const getSmaller = (num1, num2) => {
	if (num1 < num2) {
		return num1;
	}
	return num2;
}

class Particle {
	constructor() {
		this.x = getRandomNum(0, canvas.width);
		this.y = getRandomNum(0, canvas.height);
		this.z = getRandomNum(0.5, 1);
		this.r = getRandomNum(2, 6) * this.z;
		this.angle = getRandomNum(1, 360) * 0.01745;
		this.v = getRandomNum(0.5, 2);
	}

	draw() {
		context.beginPath();
		context.arc(this.x, this.y, this.r, 0, 2 * Math.PI);
		context.fillStyle = colorThemes[selectedTheme].circle;
		context.fill();
		context.shadowColor = colorThemes[selectedTheme].shadowColor;
		// context.shadowBlur = 3 * this.z;
	}

	reConf() {
		const rand = getRandomInt(1, 5);
		if (rand == 1) {
			this.x = getRandomNum(0, canvas.width);
			this.y = -10;
			this.z = getRandomNum(0.5, 1);
			this.r = getRandomNum(2, 6) * this.z;
			if (this.x / canvas.width < 0.5) {
				this.angle = getRandomNum(10, 80) * 0.01745;
			} else {
				this.angle = getRandomNum(100, 170) * 0.01745;
			}
			this.v = getRandomNum(0.5, 2);
		} else if (rand == 2) {
			this.x = canvas.width + 10;
			this.y = getRandomNum(0, canvas.height);
			this.z = getRandomNum(0.5, 1);
			this.r = getRandomNum(2, 6) * this.z;
			if (this.y / canvas.height < 0.5) {
				this.angle = getRandomNum(100, 170) * 0.01745;
			} else {
				this.angle = getRandomNum(190, 260) * 0.01745;
			}
			this.v = getRandomNum(0.5, 2);
		} else if (rand == 3) {
			this.x = getRandomNum(0, canvas.width);
			this.y = canvas.height + 10;
			this.z = getRandomNum(0.5, 1);
			this.r = getRandomNum(2, 6) * this.z;
			if (this.x / canvas.width < 0.5) {
				this.angle = getRandomNum(280, 350) * 0.01745;
			} else {
				this.angle = getRandomNum(190, 260) * 0.01745;
			}
			this.v = getRandomNum(0.5, 2);
		} else if (rand == 4) {
			this.x = -10;
			this.y = getRandomNum(0, canvas.height);
			this.z = getRandomNum(0.5, 1);
			this.r = getRandomNum(2, 6) * this.z;
			if (this.y / canvas.height < 0.5) {
				this.angle = getRandomNum(10, 80) * 0.01745;
			} else {
				this.angle = getRandomNum(280, 350) * 0.01745;
			}
			this.v = getRandomNum(0.5, 2);
		}
	}
}

class Connector {
	constructor(x1, y1, x2, y2, lineWidth) {
		this.x1 = x1;
		this.y1 = y1;
		this.x2 = x2;
		this.y2 = y2;
		this.lineWidth = lineWidth;
	}

	draw() {
		context.beginPath();
		context.moveTo(this.x1, this.y1);
		context.lineTo(this.x2, this.y2);
		context.strokeStyle = colorThemes[selectedTheme].line;
		context.lineWidth = this.lineWidth;
		context.stroke();
		context.shadowColor = colorThemes[selectedTheme].bg;
	}
}

const updateConnectorArray = () => {
	connectorObjects = null;
	connectorObjects = [];
	particleObjects.forEach(object => {
		particleObjects.forEach(objectInner => {
			if (object !== objectInner) {
				if ((object.x >= 0) && (object.y >= 0) && (objectInner.x >= 0) && (objectInner.y >= 0) && (object.x <= canvas.width) && (object.y <= canvas.height) && (objectInner.x <= canvas.width) && (objectInner.y <= canvas.height)) {
					if ((Math.abs(object.x - objectInner.x) <= 150) && (Math.abs(object.y - objectInner.y) <= 150)) {
						let lineWidth;
						if ((object.x > objectInner.x) && (object.y > objectInner.y)) {
							lineWidth = getSmaller((objectInner.x / object.x), (objectInner.y / object.y)) * 0.4;
						} else if ((object.x < objectInner.x) && (object.y < objectInner.y)) {
							lineWidth = getSmaller((object.x / objectInner.x), (object.y / objectInner.y)) * 0.4;
						}
						let check = true;
						connectorObjects.forEach(objectTest => {
							if (((objectTest.x1 == objectInner.x) && (objectTest.y1 == objectInner.y) && (objectTest.x2 == object.x) && (objectTest.y2 == object.y)) || ((objectTest.x1 == object.x) && (objectTest.y1 == object.y) && (objectTest.x2 == objectInner.x) && (objectTest.y2 == objectInner.y))) {
								check = false;
							}
						});
						if (check) {
							let newLine = new Connector(object.x, object.y, objectInner.x, objectInner.y, lineWidth);
							newLine.draw();
							connectorObjects.push(newLine);
						}
					}
				}
			}
		});
		if (mouseOver) {
			if ((object.x >= 0) && (object.y >= 0) && (object.x <= canvas.width) && (object.y <= canvas.height)) {
				if ((Math.abs(object.x - mouseX) <= canvas.width / 3 && (Math.abs(object.y - mouseY) <= canvas.height / 3))) {
					let lineWidth;
					if (Math.abs(object.x - mouseX) >= Math.abs(object.y - mouseY)) {
						if (object.x > mouseX) {
							lineWidth = (mouseX / object.x) * 0.8;
						} else if (object.x < mouseX) {
							lineWidth = (object.x / mouseX) * 0.8;
						}
					} else {
						if (object.y > mouseY) {
							lineWidth = (mouseY / object.y) * 0.8;
						} else if (object.y < mouseY) {
							lineWidth = (object.y / mouseY) * 0.8;
						}
					}
					let newLine = new Connector(object.x, object.y, mouseX, mouseY, lineWidth);
					newLine.draw();
					connectorObjects.push(newLine);
				}
			}
		}
	});
}

const clearCanvas = () => {
	context.clearRect(0, 0, canvas.width, canvas.height);
}

let lastTimestamp = 0;
let maxFPS = 61;
let timestep = 1000 / maxFPS;

const mainLoop = (timestamp) => {
	window.requestAnimationFrame(mainLoop);
	if (timestamp - lastTimestamp < timestep) return;
	lastTimestamp = timestamp;
	clearCanvas();
	updateConnectorArray();
	particleObjects.forEach(particle => {
		if ((particle.x > -11) && (particle.x < (canvas.width + 11)) && (particle.y > -11) && (particle.y < (canvas.height + 11))) {
			particle.x = particle.x + Math.cos(particle.angle) * particle.v;
			particle.y = particle.y + Math.sin(particle.angle) * particle.v;
			particle.draw();
		} else {
			particle.reConf();
			particle.draw();
		}
	});
}

const colorSwitch = () => {
	document.querySelector('body').style.backgroundColor = colorThemes[selectedTheme].bg;
	document.querySelector('p').style.color = colorThemes[selectedTheme].pFont;
	canvas.style.border = `1px solid ${colorThemes[selectedTheme].bg}`;
}

document.addEventListener('click', (event) => {
	if (selectedTheme < (colorThemes.length - 1)) {
		selectedTheme++;
	} else {
		selectedTheme = 0;
	}
	colorSwitch();
});

document.addEventListener('mousemove', (event) => {
	mouseX = event.pageX;
	mouseY = event.pageY;
	mouseOver = true;
});

document.addEventListener('mouseleave', (event) => {
	mouseOver = false;
	mouseX = 0;
	mouseY = 0;
});

document.addEventListener("keydown", function(event) {
  if (event.key.toLowerCase() == 'r') {
		if (autoChangeTheme === false) {
			autoChangeTheme = true;
			autoChangeThemeInterval = setInterval(() => {
				if (selectedTheme < (colorThemes.length - 1)) {
					selectedTheme++;
				} else {
					selectedTheme = 0;
				}
				colorSwitch();
			}, 1000);
		} else {
			clearInterval(autoChangeThemeInterval);
		}
	}
})

// resize window
let lastResizeTime = 0;
window.addEventListener('resize', (event) => {
	clearCanvas();
	canvas.width = (innerWidth - 2);
	canvas.height = (innerHeight - 2);
	particleObjects = [];
	connectorObjects = [];
	if (innerWidth >= innerHeight) {
		particleCount = parseInt(innerWidth / 20);
	} else {
		particleCount = parseInt(innerHeight / 20);
	}
	for (let i = 0; i < particleCount; i++) {
		let newParticle = new Particle();
		newParticle.draw();
		particleObjects.push(newParticle);
	}
});