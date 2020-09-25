//let lesson_pack_words = {{ lesson_pack_words|safe }}

// ^^ the code above will be added into another script tag inside the html
// because it contains djangos own templating syntax which js cant compile

let questions = [];
let answered_questions = []
let questions_canvas = document.getElementById("questions-canvas");

let check_button = document.getElementById("check-button");
let next_button = document.getElementById("next-button");
let finish_button = document.getElementById("finish-button");


// Question Data Structure
function Question(word, word_translation) {
  this.word = word;
  this.word_translation = word_translation;
  this.answer_options = [];

  // CREATING THE ANSWER OPTIONS
  function random_num() {
    return Math.floor(Math.random() * 9) + 1;
  }

  function shuffle(array) {
    let counter = array.length;
    // While there are elements in the array
    while (counter > 0) {
        // Pick a random index
        let index = Math.floor(Math.random() * counter);
        // Decrease counter by 1
        counter--;
        // And swap the last element with it
        let temp = array[counter];
        array[counter] = array[index];
        array[index] = temp;
    }
    return array;
  }

  while(this.answer_options.length < 3) {
    let num = random_num();
    let key = Object.keys(lesson_pack_words)[num];
    // if the value is same as answer do not push pick another
    // elseif the value is already in the answe options do it again
    if (lesson_pack_words[key] == this.word_translation) {
      continue;
    }
    else if(this.answer_options.includes(lesson_pack_words[key]) == true) {
      continue;
    }
    else {
      this.answer_options.push(lesson_pack_words[key]);
    }
  }
  // add the "correct answer" to the options
  this.answer_options.push(this.word_translation);
  // shuffle the array
  this.answer_options = shuffle(this.answer_options);

  this.get_question = function() {
    return this.word;
  }
  this.get_answer = function() {
    return this.word_translation;
  }
  this.get_options = function() {
    return this.answer_options;
  }
  this.get_question_slide = function() {
    answers = this.get_options();
    slide_template = `<div id="middle-part">
        <h3>${this.get_question()}</h3>
        <div id="middle-part-answer-selections">
          <div class="answer-cell" id="answer-1" tabindex="1">
            <p><span id="answer-select-color">1</span>${answers[0]}</p>
          </div>
          <div class="answer-cell" id="answer-2" tabindex="1">
            <p><span id="answer-select-color">2</span>${answers[1]}</p>
          </div>
          <div class="answer-cell" id="answer-3" tabindex="1">
            <p><span id="answer-select-color">3</span>${answers[2]}</p>
          </div>
          <div class="answer-cell" id="answer-4" tabindex="1">
            <p><span id="answer-select-color">4</span>${answers[3]}</p>
          </div>
        </div>
      </div>`;
    return slide_template;
  }
}

// building the Question List
let size = Object.keys(lesson_pack_words).length;
for (let i=0; i < size; i++) {
  let key = Object.keys(lesson_pack_words)[i];
  new_question = new Question(key, lesson_pack_words[key]);
  questions.push(new_question);
}

// loop the slides untill all of the questions are answered correcly

// get the current question
current_question = questions[0];

// get the current slide and display it
questions_canvas.innerHTML = current_question.get_question_slide();

// get the selected answer
answer_options = current_question.get_options();

var answer_1 = document.getElementById("answer-1");
var answer_2 = document.getElementById("answer-2");
var answer_3 = document.getElementById("answer-3");
var answer_4 = document.getElementById("answer-4");
var selected_answer = null;

answer_1.onclick = function() {
  selected_answer = answer_options[0];
};

answer_2.onclick = function() {
  selected_answer = answer_options[1];
};

answer_3.onclick = function() {
  selected_answer = answer_options[2];
};

answer_4.onclick = function() {
  selected_answer = answer_options[3];
};

// if check button is clicked show if the answer is true or not
check_button.onclick = function() {
  // if the lenght is 10 and lesson is finished submit it to backend
  if (answered_questions.length === 10) {
    check_button.style.display = "none";
    next_button.style.display = "none";
    finish_button.style.display = "block";
  }

  answer_1.onclick = function() {
    selected_answer = answer_options[0];
  };

  answer_2.onclick = function() {
    selected_answer = answer_options[1];
  };

  answer_3.onclick = function() {
    selected_answer = answer_options[2];
  };

  answer_4.onclick = function() {
    selected_answer = answer_options[3];
  };

  // ANSWERED CORRECTLY
  if (selected_answer === current_question.get_answer()) {

    // show the right answers
    if (selected_answer == answer_options[0]) {
      answer_1.style.backgroundColor = "#27AE60";
      answer_1.style.color = "white";
    }
    else if (selected_answer == answer_options[1] ) {
      answer_2.style.backgroundColor = "#27AE60";
      answer_2.style.color = "white";
    }
    else if (selected_answer == answer_options[2] ) {
      answer_3.style.backgroundColor = "#27AE60";
      answer_3.style.color = "white";
    }
    else if (selected_answer == answer_options[3] ) {
      answer_4.style.backgroundColor = "#27AE60";
      answer_4.style.color = "white";
    }
    // add the current question to the answered questions
    answered_questions.push(current_question);

    // turn the check button to next button
    check_button.style.display = "none";
    next_button.style.display = "block";
  }
  else {
    // show the right answers
    if (selected_answer == answer_options[0]) {
      answer_1.style.backgroundColor = "#E3102E";
      answer_1.style.color = "black";
    }
    else if (selected_answer == answer_options[1] ) {
      answer_2.style.backgroundColor = "#E3102E";
      answer_1.style.color = "black";
    }
    else if (selected_answer == answer_options[2] ) {
      answer_3.style.backgroundColor = "#E3102E";
      answer_1.style.color = "black";
    }
    else if (selected_answer == answer_options[3] ) {
      answer_4.style.backgroundColor = "#E3102E";
      answer_1.style.color = "black";
    }
    // turn the right answer to green
    real_answer = current_question.get_answer();

    if (answer_1.innerText.slice(2) == real_answer) {
      answer_1.style.backgroundColor = "#27AE60";
      answer_1.style.color = "white";
    }
    else if (answer_2.innerText.slice(2) == real_answer) {
      answer_2.style.backgroundColor = "#27AE60";
      answer_2.style.color = "white";
    }
    else if (answer_3.innerText.slice(2) == real_answer) {
      answer_3.style.backgroundColor = "#27AE60";
      answer_3.style.color = "white";
    }
    else if (answer_4.innerText.slice(2) == real_answer) {
      answer_4.style.backgroundColor = "#27AE60";
      answer_4.style.color = "white";
    }
    // turn the check button to next button
    check_button.style.display = "none";
    next_button.style.display = "block";
  }
};

// next button removes if the question is answered correctly and cycles
// thorugh the questions
// function for making the questions array endless cycle
strIndex = 0;
function get_next_question() {
  // If you reached the end of the array, reset to 0
  if (strIndex === questions.length - 1) {
    strIndex = 0;
    return questions[strIndex];
  }
  // Otherwise, increment it and return the new value
  else return questions[++strIndex];
}

next_button.onclick = function() {
  // if the lenght is 10 and lesson is finished submit it to backend
  if (answered_questions.length === 10) {
    check_button.style.display = "none";
    next_button.style.display = "none";
    finish_button.style.display = "block";
  }

  var progress_bar = document.getElementById("progress-bar");
  var progress_status = document.getElementById("progress-status");

  // based on how many questions lenght update progress status
  if (answered_questions.length === 0) {
    progress_status.style.width = "0%";
  }
  else if (answered_questions.length === 1) {
    progress_status.style.width = "10%";
  }
  else if (answered_questions.length === 2) {
    progress_status.style.width = "20%";
  }
  else if (answered_questions.length === 3) {
    progress_status.style.width = "30%";
  }
  else if (answered_questions.length === 4) {
    progress_status.style.width = "40%";
  }
  else if (answered_questions.length === 5) {
    progress_status.style.width = "50%";
  }
  else if (answered_questions.length === 6) {
    progress_status.style.width = "60%";
  }
  else if (answered_questions.length === 7) {
    progress_status.style.width = "70%";
  }
  else if (answered_questions.length === 8) {
    progress_status.style.width = "80%";
  }
  else if (answered_questions.length === 9) {
    progress_status.style.width = "90%";
  }
  else if (answered_questions.length === 10) {
    progress_status.style.width = "100%";
  }

  // get the current question and get the next one
  // if the next one is in
  // current_question = get_next_question();
  iteration_count = 0;
  while(true) {
    current_question = get_next_question();

    if (iteration_count == 10) {
      break;
    }

    if (answered_questions.includes(current_question) == true) {
      current_question = get_next_question();
      iteration_count++;
    } else {
      // found an unanswered questions break!
      break;
    }
  }

  // get the current slide and display it
  questions_canvas.innerHTML = current_question.get_question_slide();

  // get new answer options
  answer_options = current_question.get_options();

  answer_1 = document.getElementById("answer-1");
  answer_2 = document.getElementById("answer-2");
  answer_3 = document.getElementById("answer-3");
  answer_4 = document.getElementById("answer-4");

  selected_answer = null;

  answer_1.onclick = function() {
    selected_answer = answer_options[0];
  };

  answer_2.onclick = function() {
    selected_answer = answer_options[1];
  };

  answer_3.onclick = function() {
    selected_answer = answer_options[2];
  };

  answer_4.onclick = function() {
    selected_answer = answer_options[3];
  };

  // turn the check button to next button
  if (answered_questions.length === 10) {
    check_button.style.display = "none";
  } else {
    check_button.style.display = "block";
  }
  next_button.style.display = "none";
};
