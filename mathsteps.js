const mathsteps = require('mathsteps');

const steps = mathsteps.simplifyExpression(process.argv[2].replace(/\*\*/g, '^'));
//console.log(process.argv[2])
//console.log(typeof(process.argv[2]))
//console.log(steps)

steps.forEach(step => {
	console.log(step.newNode.toString());    // after change: 6 x
});

/*

const steps = mathsteps.simplifyExpression('j^(-2/7)*j*j^(-14)*j^(2/29)*j^(-2)');

steps.forEach(step => {
	console.log("after change: " + step.newNode.toString());    // after change: 6 x
});*/