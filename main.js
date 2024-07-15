let standingsData;

// JSONデータを読み込む
fetch("atcoder_standings.json")
  .then((response) => response.json())
  .then((data) => {
    standingsData = data;
    populateContestSelector();
    showRankings(Object.keys(standingsData)[0]); // 最初のコンテストを表示
  });

// コンテストセレクターを生成する
function populateContestSelector() {
  const selector = document.getElementById("contestSelector");
  for (let contestId in standingsData) {
    const option = document.createElement("option");
    option.value = contestId;
    option.textContent = contestId;
    selector.appendChild(option);
  }
  selector.addEventListener("change", (e) => showRankings(e.target.value));
}

// 順位表を表示する
function showRankings(contestId) {
  const contestData = standingsData[contestId];
  document.getElementById("contestTitle").textContent = `${contestId} (${contestData.date})`;

  const tbody = document.getElementById("rankingBody");
  tbody.innerHTML = ""; // テーブルをクリア

  contestData.rankings.forEach((entry) => {
    const row = tbody.insertRow();
    row.insertCell(0).textContent = entry.rank;
    row.insertCell(1).textContent = entry.username;
  });
}
