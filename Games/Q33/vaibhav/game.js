const tasks = [
    {
        title: "Task 1: Help the Patient",
        description: "A student is feeling sick. What would you do to help them feel better?",
        gif: 'sick.gif',
        options: [
            { image: 'medicine.gif', profession: 'doctor' },
            { image: 'phone.gif', profession: 'doctor' },
            { image: 'rest.gif', profession: 'doctor' }
        ]
    },
    {
        title: "Task 2: Build a Simple Bridge",
        description: "You need to build a bridge using blocks. What is your plan?",
        gif: 'bridge.gif',
        options: [
            { image: 'pillar.gif', profession: 'engineer' },
            { image: 'blocks.gif', profession: 'engineer' },
            { image: 'design.gif', profession: 'engineer' }
        ]
    },
    {
        title: "Task 3: Plan a School Event",
        description: "You are organizing a school fair. What steps will you take?",
        gif: 'schooltrip.gif',
        options: [
            { image: 'budget.gif', profession: 'businessman' },
            { image: 'activities.gif', profession: 'businessman' },
            { image: 'guests.gif', profession: 'businessman' }
        ]
    },
    {
        title: "Task 4: Organize a Community Cleanup",
        description: "You want to help clean up your local park. What will you do?",
        gif: 'scholltrip.gif',
        options: [
            { image: 'budget.gif', profession: 'socialworker' },
            { image: 'activities.gif', profession: 'socialworker' },
            { image: 'guests.gif', profession: 'socialworker' }
        ]
    }
];

let currentTaskIndex = 0;
const scores = { doctor: 0, engineer: 0, businessman: 0, socialworker: 0 };

function startGame() {
    currentTaskIndex = 0;
    scores.doctor = 0;
    scores.engineer = 0;
    scores.businessman = 0;
    scores.socialworker = 0;
    document.getElementById('start-button').style.display = 'none';
    showTask();
}

function showTask() {
    if (currentTaskIndex < tasks.length) {
        const task = tasks[currentTaskIndex];
        document.getElementById('task-title').innerText = task.title;
        document.getElementById('task-description').innerText = task.description;
        document.getElementById('task-gif').src = task.gif;

        const optionsContainer = document.getElementById('options-container');
        optionsContainer.innerHTML = '';

        task.options.forEach((option) => {
            const optionDiv = document.createElement('div');
            optionDiv.classList.add('option');
            optionDiv.setAttribute('draggable', 'true');
            optionDiv.setAttribute('data-profession', option.profession);

            const img = document.createElement('img');
            img.src = option.image;
            optionDiv.appendChild(img);

            optionDiv.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', option.profession);
                e.dataTransfer.setData('text/image', option.image);
            });

            optionsContainer.appendChild(optionDiv);
        });

        const dropArea = document.getElementById('task-gif');
        dropArea.setAttribute('data-task-profession', task.options[0].profession); // Assuming all options are for the same profession

        dropArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropArea.classList.add('drag-over');
        });
        dropArea.addEventListener('dragleave', () => {
            dropArea.classList.remove('drag-over');
        });
        dropArea.addEventListener('drop', (e) => {
            e.preventDefault();
            dropArea.classList.remove('drag-over');
            const profession = e.dataTransfer.getData('text/plain');
            scores[profession]++;
            currentTaskIndex++;
            showTask();
        });
    } else {
        showResult();
    }
}

function showResult() {
    const maxScore = Math.max(scores.doctor, scores.engineer, scores.businessman, scores.socialworker);
    const predictedProfession = Object.keys(scores).find(key => scores[key] === maxScore);
    
    const resultData = {
        doctor: {
            text: "You seem to have an interest in helping others and solving problems related to health. A career as a doctor might be a great fit for you!",
            image: 'doctor-career.gif'
        },
        engineer: {
            text: "You enjoy solving practical problems and building things. Consider a career as an engineer where you can apply these skills!",
            image: 'engineer-career.gif'
        },
        businessman: {
            text: "You have a knack for organizing events and making decisions. A career in business might be your calling!",
            image: 'businessman-career.gif'
        },
        socialworker: {
            text: "You like helping and organizing community activities. A career in social work could be a great fit for you!",
            image: 'socialworker-career.gif'
        }
    };

    document.getElementById('task-container').style.display = 'none';
    document.getElementById('result-text').innerText = resultData[predictedProfession].text;
    document.getElementById('result-image').src = resultData[predictedProfession].image;
    document.getElementById('result-container').style.display = 'block';
}
