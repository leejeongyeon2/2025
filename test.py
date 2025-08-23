<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>단어 암기 앱</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
    #card { width: 200px; height: 120px; margin: 20px auto; border: 2px solid #333;
      border-radius: 10px; display: flex; align-items: center; justify-content: center;
      font-size: 20px; cursor: pointer; background: #f9f9f9; }
    button { margin: 5px; padding: 8px 15px; border: none; border-radius: 8px; background: #4CAF50; color: white; cursor: pointer; }
    button:hover { background: #45a049; }
    .hidden { display: none; }
  </style>
</head>
<body>
  <h1>📚 단어 암기 앱</h1>

  <div>
    <input id="wordInput" placeholder="단어 입력">
    <input id="meaningInput" placeholder="뜻 입력">
    <button onclick="addWord()">추가</button>
  </div>

  <h2>플래시카드</h2>
  <div id="card" onclick="flipCard()">
    <p id="front"></p>
    <p id="back" class="hidden"></p>
  </div>
  <button onclick="nextWord()">다음 단어</button>

  <h2>퀴즈 모드</h2>
  <p id="quizWord"></p>
  <div id="options"></div>

  <h3>통계</h3>
  <p>맞춘 개수: <span id="correct">0</span> | 틀린 개수: <span id="wrong">0</span></p>

  <script>
    let words = JSON.parse(localStorage.getItem("words")) || [
      {word: "apple", meaning: "사과"},
      {word: "book", meaning: "책"},
      {word: "school", meaning: "학교"}
    ];
    let currentIndex = 0;
    let flipped = false;
    let correct = 0, wrong = 0;

    function saveWords() {
      localStorage.setItem("words", JSON.stringify(words));
    }

    function addWord() {
      const w = document.getElementById("wordInput").value.trim();
      const m = document.getElementById("meaningInput").value.trim();
      if (w && m) {
        words.push({word: w, meaning: m});
        saveWords();
        document.getElementById("wordInput").value = "";
        document.getElementById("meaningInput").value = "";
        alert("단어가 추가되었습니다!");
        showCard();
        makeQuiz();
      }
    }

    function showCard() {
      const front = document.getElementById("front");
      const back = document.getElementById("back");
      front.textContent = words[currentIndex].word;
      back.textContent = words[currentIndex].meaning;
      front.classList.remove("hidden");
      back.classList.add("hidden");
      flipped = false;
    }

    function flipCard() {
      flipped = !flipped;
      document.getElementById("front").classList.toggle("hidden", flipped);
      document.getElementById("back").classList.toggle("hidden", !flipped);
    }

    function nextWord() {
      currentIndex = (currentIndex + 1) % words.length;
      showCard();
    }

    function makeQuiz() {
      const qWord = words[Math.floor(Math.random() * words.length)];
      document.getElementById("quizWord").textContent = `단어: ${qWord.word}`;

      let options = [qWord.meaning];
      while (options.length < 4 && options.length < words.length) {
        let m = words[Math.floor(Math.random() * words.length)].meaning;
        if (!options.includes(m)) options.push(m);
      }
      options.sort(() => Math.random() - 0.5);

      const optDiv = document.getElementById("options");
      optDiv.innerHTML = "";
      options.forEach(o => {
        const btn = document.createElement("button");
        btn.textContent = o;
        btn.onclick = () => checkAnswer(o, qWord.meaning);
        optDiv.appendChild(btn);
      });
    }

    function checkAnswer(choice, answer) {
      if (choice === answer) {
        correct++;
        alert("정답!");
      } else {
        wrong++;
        alert(`오답! 정답은: ${answer}`);
      }
      document.getElementById("correct").textContent = correct;
      document.getElementById("wrong").textContent = wrong;
      makeQuiz();
    }

    // 초기 실행
    showCard();
    makeQuiz();
  </script>
</body>
</html>
