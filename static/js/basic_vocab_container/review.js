// let lesson_pack_words = {{ review_pack_words|safe }};
// let current_lesson_length = {{ current_lesson_length|safe }};

// ^^ the code above will be added into another script tag inside the html
// because it contains djangos own templating syntax which js cant compile

let body_element = document.getElementsByTagName("BODY")[0];

let questions = [];
let answered_questions = [];
let errors = [];
let questions_canvas = document.getElementById("questions-canvas");

let check_button = document.getElementById("check-button");
let next_button = document.getElementById("next-button");
let finish_button = document.getElementById("finish-button");

let error_report_button = document.getElementById("error-report-btn");
var panel = document.getElementById("hidden-error-panel");
var panel_background_greying = document.getElementById("background-greying");
let hidden_errors_input = document.getElementById("hidden_errors_input");

let current_page_state = "check";

// Error Data Scturcutre
function Error(question, content) {
    this.question = question;
    this.content = content;

    this.get_question = function() {
      return this.question;
    };
    this.get_content = function(){
      return this.content;
    };
}

// Question Data Structure
function Question(word, word_translation) {
  this.word = word;
  this.word_translation = word_translation;
  this.answer_options = [];

  // CREATING THE ANSWER OPTIONS
  let size = Object.keys(lesson_pack_words).length;
  function random_num() {
    return Math.floor(Math.random() * size-1) + 1;
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
  };
  this.get_answer = function() {
    return this.word_translation;
  };
  this.get_options = function() {
    return this.answer_options;
  };

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
  };
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

// selected answer color changes
function selected_answer_1_colors() {
  answer_1.style.backgroundColor = "black";
  answer_1.style.color = "white";
  answer_2.style.backgroundColor = "white";
  answer_2.style.color = "black";
  answer_3.style.backgroundColor = "white";
  answer_3.style.color = "black";
  answer_4.style.backgroundColor = "white";
  answer_4.style.color = "black";
}

function selected_answer_2_colors() {
  answer_1.style.backgroundColor = "white";
  answer_1.style.color = "black";
  answer_2.style.backgroundColor = "black";
  answer_2.style.color = "white";
  answer_3.style.backgroundColor = "white";
  answer_3.style.color = "black";
  answer_4.style.backgroundColor = "white";
  answer_4.style.color = "black";
}

function selected_answer_3_colors() {
  answer_1.style.backgroundColor = "white";
  answer_1.style.color = "black";
  answer_2.style.backgroundColor = "white";
  answer_2.style.color = "black";
  answer_3.style.backgroundColor = "black";
  answer_3.style.color = "white";
  answer_4.style.backgroundColor = "white";
  answer_4.style.color = "black";
}

function selected_answer_4_colors() {
  answer_1.style.backgroundColor = "white";
  answer_1.style.color = "black";
  answer_2.style.backgroundColor = "white";
  answer_2.style.color = "black";
  answer_3.style.backgroundColor = "white";
  answer_3.style.color = "black";
  answer_4.style.backgroundColor = "black";
  answer_4.style.color = "white";
}

answer_1.onclick = function() {
  selected_answer = answer_options[0];
  selected_answer_1_colors();
};

answer_2.onclick = function() {
  selected_answer = answer_options[1];
  selected_answer_2_colors();
};

answer_3.onclick = function() {
  selected_answer = answer_options[2];
  selected_answer_3_colors();
};

answer_4.onclick = function() {
  selected_answer = answer_options[3];
  selected_answer_4_colors();
};

// change selected answer if there is a keyboard access
body_element.onkeydown = function(event) {
  let key = event.key;

  // answer slection logic for key presses
  if (key == "1") {
    selected_answer = answer_options[0];
    selected_answer_1_colors();
  }
  else if (key == "2") {
    selected_answer = answer_options[1];
    selected_answer_2_colors();
  }
  else if (key == "3") {
    selected_answer = answer_options[2];
    selected_answer_3_colors();
  }
  else if (key == "4") {
    selected_answer = answer_options[3];
    selected_answer_4_colors();
  }

  // check and next buttons logic for key presses
  if (key == "Enter") {
    if (current_page_state == "check") {
      checking_logic();
      current_page_state = "next";
    }
    else if (current_page_state == "next") {
      next_logic();
      current_page_state = "check";
    }
  }
};

// if check button is clicked show if the answer is true or not
check_button.onclick = function() {
  checking_logic();
}

function checking_logic() {
  // if the lenght is 10 and lesson is finished submit it to backend
  let size = Object.keys(lesson_pack_words).length;
  if (answered_questions.length === size) {
    check_button.style.display = "none";
    next_button.style.display = "none";
    finish_button.style.display = "block";
  }

  answer_1.onclick = function() {
    selected_answer = answer_options[0];
    selected_answer_1_colors();
  };

  answer_2.onclick = function() {
    selected_answer = answer_options[1];
    selected_answer_2_colors();
  };

  answer_3.onclick = function() {
    selected_answer = answer_options[2];
    selected_answer_3_colors();
  };

  answer_4.onclick = function() {
    selected_answer = answer_options[3];
    selected_answer_4_colors();
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
  next_logic();
}

function next_logic() {
  // if the lenght is 10 and lesson is finished submit it to backend
  let size = Object.keys(lesson_pack_words).length;
  if (answered_questions.length === size) {
    check_button.style.display = "none";
    next_button.style.display = "none";
    finish_button.style.display = "block";
  }

  var progress_bar = document.getElementById("progress-bar");
  var progress_status = document.getElementById("progress-status");

  // Based on the lesson size adjust the progress bar status
  if (current_lesson_length == 5) {
    if (answered_questions.length === 0) {
      progress_status.style.width = "0%";
    }
    else if (answered_questions.length === 1) {
      progress_status.style.width = "20%";
    }
    else if (answered_questions.length === 2) {
      progress_status.style.width = "40%";
    }
    else if (answered_questions.length === 3) {
      progress_status.style.width = "60%";
    }
    else if (answered_questions.length === 4) {
      progress_status.style.width = "80%";
    }
    else if (answered_questions.length === 5) {
      progress_status.style.width = "100%";
    }
  }
  else if (current_lesson_length == 10) {
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
  }
  else if (current_lesson_length == 15) {
    if (answered_questions.length === 0) {
      progress_status.style.width = "0%";
    }
    else if (answered_questions.length === 1) {
      progress_status.style.width = "7%";
    }
    else if (answered_questions.length === 2) {
      progress_status.style.width = "14%";
    }
    else if (answered_questions.length === 3) {
      progress_status.style.width = "21%";
    }
    else if (answered_questions.length === 4) {
      progress_status.style.width = "28%";
    }
    else if (answered_questions.length === 5) {
      progress_status.style.width = "35%";
    }
    else if (answered_questions.length === 6) {
      progress_status.style.width = "42%";
    }
    else if (answered_questions.length === 7) {
      progress_status.style.width = "50%";
    }
    else if (answered_questions.length === 8) {
      progress_status.style.width = "57%";
    }
    else if (answered_questions.length === 9) {
      progress_status.style.width = "64%";
    }
    else if (answered_questions.length === 10) {
      progress_status.style.width = "71%";
    }
    else if (answered_questions.length === 11) {
      progress_status.style.width = "78%";
    }
    else if (answered_questions.length === 12) {
      progress_status.style.width = "85%";
    }
    else if (answered_questions.length === 13) {
      progress_status.style.width = "92%";
    }
    else if (answered_questions.length === 14) {
      progress_status.style.width = "96%";
    }
    else if (answered_questions.length === 15) {
      progress_status.style.width = "100%";
    }
  }
  else if (current_lesson_length == 20) {
    if (answered_questions.length === 0) {
      progress_status.style.width = "0%";
    }
    else if (answered_questions.length === 1) {
      progress_status.style.width = "5%";
    }
    else if (answered_questions.length === 2) {
      progress_status.style.width = "10%";
    }
    else if (answered_questions.length === 3) {
      progress_status.style.width = "15%";
    }
    else if (answered_questions.length === 4) {
      progress_status.style.width = "20%";
    }
    else if (answered_questions.length === 5) {
      progress_status.style.width = "25%";
    }
    else if (answered_questions.length === 6) {
      progress_status.style.width = "30%";
    }
    else if (answered_questions.length === 7) {
      progress_status.style.width = "35%";
    }
    else if (answered_questions.length === 8) {
      progress_status.style.width = "40%";
    }
    else if (answered_questions.length === 9) {
      progress_status.style.width = "45%";
    }
    else if (answered_questions.length === 10) {
      progress_status.style.width = "50%";
    }
    else if (answered_questions.length === 11) {
      progress_status.style.width = "55%";
    }
    else if (answered_questions.length === 12) {
      progress_status.style.width = "60%";
    }
    else if (answered_questions.length === 13) {
      progress_status.style.width = "65%";
    }
    else if (answered_questions.length === 14) {
      progress_status.style.width = "70%";
    }
    else if (answered_questions.length === 15) {
      progress_status.style.width = "75%";
    }
    else if (answered_questions.length === 16) {
      progress_status.style.width = "80%";
    }
    else if (answered_questions.length === 17) {
      progress_status.style.width = "85%";
    }
    else if (answered_questions.length === 18) {
      progress_status.style.width = "90%";
    }
    else if (answered_questions.length === 19) {
      progress_status.style.width = "95%";
    }
    else if (answered_questions.length === 20) {
      progress_status.style.width = "100%";
    }
  }
  else if (current_lesson_length == 25) {
    if (answered_questions.length === 0) {
      progress_status.style.width = "0%";
    }
    else if (answered_questions.length === 1) {
      progress_status.style.width = "8%";
    }
    else if (answered_questions.length === 2) {
      progress_status.style.width = "12%";
    }
    else if (answered_questions.length === 3) {
      progress_status.style.width = "16%";
    }
    else if (answered_questions.length === 4) {
      progress_status.style.width = "20%";
    }
    else if (answered_questions.length === 5) {
      progress_status.style.width = "24%";
    }
    else if (answered_questions.length === 6) {
      progress_status.style.width = "28%";
    }
    else if (answered_questions.length === 7) {
      progress_status.style.width = "32%";
    }
    else if (answered_questions.length === 8) {
      progress_status.style.width = "36%";
    }
    else if (answered_questions.length === 9) {
      progress_status.style.width = "40%";
    }
    else if (answered_questions.length === 10) {
      progress_status.style.width = "44%";
    }
    else if (answered_questions.length === 11) {
      progress_status.style.width = "48%";
    }
    else if (answered_questions.length === 12) {
      progress_status.style.width = "52%";
    }
    else if (answered_questions.length === 13) {
      progress_status.style.width = "56%";
    }
    else if (answered_questions.length === 14) {
      progress_status.style.width = "60%";
    }
    else if (answered_questions.length === 15) {
      progress_status.style.width = "64%";
    }
    else if (answered_questions.length === 16) {
      progress_status.style.width = "68%";
    }
    else if (answered_questions.length === 17) {
      progress_status.style.width = "72%";
    }
    else if (answered_questions.length === 18) {
      progress_status.style.width = "76%";
    }
    else if (answered_questions.length === 19) {
      progress_status.style.width = "80%";
    }
    else if (answered_questions.length === 20) {
      progress_status.style.width = "84%";
    }
    else if (answered_questions.length === 21) {
      progress_status.style.width = "88%";
    }
    else if (answered_questions.length === 22) {
      progress_status.style.width = "92%";
    }
    else if (answered_questions.length === 23) {
      progress_status.style.width = "96%";
    }
    else if (answered_questions.length === 24) {
      progress_status.style.width = "98%";
    }
    else if (answered_questions.length === 25) {
      progress_status.style.width = "100%";
    }
  }

  // get the current question and get the next one
  // if the next one is in
  // current_question = get_next_question();
  iteration_count = 0;
  while(true) {
    current_question = get_next_question();

    if (iteration_count == size) {
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
    selected_answer_1_colors();
  };

  answer_2.onclick = function() {
    selected_answer = answer_options[1];
    selected_answer_2_colors();
  };

  answer_3.onclick = function() {
    selected_answer = answer_options[2];
    selected_answer_3_colors();
  };

  answer_4.onclick = function() {
    selected_answer = answer_options[3];
    selected_answer_4_colors();
  };

  // turn the check button to next button
  if (answered_questions.length === size) {
    check_button.style.display = "none";
  } else {
    check_button.style.display = "block";
  }
  next_button.style.display = "none";
}


// Error Button onclick logic
error_report_button.onclick = function() {
  current_error_content = document.getElementById("error-content");
  new_error = new Error(current_question.word, current_error_content.value);
  errors.push(new_error);

  current_error_content.value = null;
  panel.style.display = "none";
  panel_background_greying.style.display = "none";

  // set the errors to the hidden input
  hidden_errors_input.value = JSON.stringify(errors);
}
