const roleData = {
    doctor: {
        scenario: 'You are a doctor diagnosing and treating patients. What is your first action?',
        image: 'path/to/doctor-gif.gif',
        resultText: 'You have chosen to be a doctor. You enjoy helping people and solving medical problems!',
        resultImage: 'path/to/doctor-image.jpg'
    },
    engineer: {
        scenario: 'You are an engineer working on a new project. What is your first step?',
        image: 'path/to/engineer-gif.gif',
        resultText: 'You have chosen to be an engineer. You like designing and building solutions!',
        resultImage: 'path/to/engineer-image.jpg'
    },
    businessman: {
        scenario: 'You are a businessman making crucial decisions for your company. What will you do first?',
        image: 'path/to/businessman-gif.gif',
        resultText: 'You have chosen to be a businessman. You enjoy strategy and managing business operations!',
        resultImage: 'path/to/businessman-image.jpg'
    },
    socialworker: {
        scenario: 'You are a social worker assisting individuals in need. What is your approach?',
        image: 'path/to/socialworker-gif.gif',
        resultText: 'You have chosen to be a social worker. You are passionate about helping and supporting others!',
        resultImage: 'path/to/socialworker-image.jpg'
    }
};

function startRolePlay(role) {
    if (roleData[role]) {
        const data = roleData[role];
        document.getElementById('scenario-text').innerText = data.scenario;
        document.getElementById('scenario-image').src = data.image;
        document.getElementById('result-text').innerText = data.resultText;
        document.getElementById('result-image').src = data.resultImage;
    }
}
