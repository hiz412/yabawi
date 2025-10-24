from IPython.display import HTML

HTML('''
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>야바위 게임</title>
<style>
  body {
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
  }

  #game {
    position: relative;
    width: 600px;
    height: 300px;
    background-color: white;
    border: 2px solid #000;
    overflow: hidden;
  }

  .cup {
    position: absolute;
    bottom: 0;
    width: 100px;
    height: 100px;
    background-color: #999;
    border-radius: 10px;
    cursor: pointer;
    transition: left 0.8s ease-in-out;
  }

  #cup1 { left: 100px; }
  #cup2 { left: 250px; }
  #cup3 { left: 400px; }

  #ball {
    position: absolute;
    bottom: 100px;
    left: 250px;
    width: 30px;
    height: 30px;
    background-color: red;
    border-radius: 50%;
    display: none;
    transition: left 0.8s ease-in-out;
  }

  button {
    position: absolute;
    bottom: -60px;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 20px;
    font-size: 18px;
    cursor: pointer;
  }
</style>
</head>
<body>

<div id="game">
  <div id="cup1" class="cup"></div>
  <div id="cup2" class="cup"></div>
  <div id="cup3" class="cup"></div>
  <div id="ball"></div>
  <button onclick="shuffle()">섞기</button>
</div>

<script>
let ballPos = 2; // 1, 2, 3 중 하나 (공 위치)
let cups = [document.getElementById("cup1"),
            document.getElementById("cup2"),
            document.getElementById("cup3")];
let ball = document.getElementById("ball");
let animating = false;

function shuffle() {
  if (animating) return;
  animating = true;
  ball.style.display = "none";

  let moves = 5;
  let count = 0;

  let shuffleInterval = setInterval(() => {
    let i = Math.floor(Math.random() * 3);
    let j = Math.floor(Math.random() * 3);
    if (i !== j) {
      let tempLeft = cups[i].style.left;
      cups[i].style.left = cups[j].style.left;
      cups[j].style.left = tempLeft;

      if (ballPos === i + 1) ballPos = j + 1;
      else if (ballPos === j + 1) ballPos = i + 1;
      count++;
    }
    if (count >= moves) {
      clearInterval(shuffleInterval);
      animating = false;
      setTimeout(() => alert("이제 어느 컵에 공이 있을까요?"), 500);
    }
  }, 1000);
}

cups.forEach((cup, index) => {
  cup.addEventListener("click", () => {
    if (animating) return;
    if (ballPos === index + 1) {
      ball.style.display = "block";
      ball.style.left = cup.style.left;
      alert("정답! 🎉");
    } else {
      alert("틀렸어요 😢 다시 시도해보세요!");
    }
  });
});
</script>

</body>
</html>
''')
