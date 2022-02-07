"use strict";


class GameView {
    constructor() {
        this.initComponents();


        this.gameInProcess = true;
    }

    initComponents() {
        this.userName = document.getElementById("username").value;
        this.hostName = document.getElementById("hostname").value;

        this.$chatMessageContainer = document.getElementById("chat-messages");
        this.$chatMessageToSend = document.getElementById("chat-message-input");


        this.$helpControl = document.getElementById("help-control");
        this.$helpControl.addEventListener("click", this.showHelp.bind(this));
        this.$helpOverlay = document.getElementById("rules-overlay");
        this.showingHelp = false;

        if (this.userName === this.hostName) {
            this.$exitControl = document.getElementById("exit-control");
            this.$exitControl.addEventListener("click", this.endGame.bind(this));
        }

        this.$chatMessageToSend.addEventListener("keydown", e => {
            const key = e.which || e.keyCode;
            // Detect Enter pressed
            if (key === 13) this.sendMessage();
        });


        this.$usersContainer = document.getElementById("users-container");

        this.$modalCard = document.getElementById("modal-card");
        this.$modalCardContent = document.querySelector("#modal-card .card-content-container");
        this.$modalAvatar = document.getElementById("modal-user-avatar");
        this.$modalMessage = document.getElementById("modal-message-container");
        this.$modalButtons = document.getElementById("modal-buttons-container");
        this.$modalTitle = document.getElementById("modal-title");
        this.$modalSubTitle = document.getElementById("modal-subtitle");

        this.showModal(null, "Welcome to Monopoly", "", "Loading game resources...", []);
        this.initBoard();
    }

    initBoard() {
        this.gameController = new GameController({
            // The DOM element in which the drawing will happen.
            containerEl: document.getElementById("game-container"),

            // The base URL from where the BoardController will load its data.
            assetsUrl: "/static/3d_assets",

            onBoardPainted: this.initWebSocket.bind(this)
        });

        window.addEventListener("resize", () => {
            this.gameController.resizeBoard();
        }, false);
    }

    initWebSocket() {
        this.socket = new WebSocket(`ws://${window.location.host}/game/${this.hostName}`);

        this.socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
        };
    }


    /*
    * Add a chat message
    * playerIndex: int
    * message: string
    * */
    addChatMessage(playerIndex, message) {
        let messageElement = document.createElement("div");
        messageElement.classList.add("chat-message");
        messageElement.innerHTML = `
            <img class="chat-message-avatar" src="/static/images/player_${playerIndex}.png">
            <span class="chat-message-content">${message}</span>`;
        this.$chatMessageContainer.appendChild(messageElement);
    }

    sendMessage() {
        const message = this.$chatMessageToSend.value;
        this.socket.send(JSON.stringify({
            action: "chat",
            from: this.myPlayerIndex,
            content: message,
        }));
        this.$chatMessageToSend.value = "";
    }
      showModal(playerIndex, title, subTitle, message, buttons, displayTime) {
        return new Promise(resolve => {


            this.$modalMessage.innerHTML = message;
            this.$modalButtons.innerHTML = "";

            this.$modalTitle.innerText = title;
            this.$modalSubTitle.innerText = subTitle;

            for (let i in buttons) {
                let button = document.createElement("button");
                button.classList.add("large-button");
                button.id = `modal-button-${i}`;
                button.innerText = buttons[i].text;

                button.addEventListener("click", () => {
                    buttons[i].callback();
                    resolve();
                });


                this.$modalButtons.appendChild(button);
            }

            this.$modalCard.classList.remove("hidden");
            this.$modalCard.classList.remove("modal-hidden");

            // hide modal after a period of time if displayTime is set
            if (displayTime !== undefined && displayTime > 0) {
                setTimeout(async () => {
                    await this.hideModal(true);
                    resolve();
                }, displayTime * 1000);
            } else {
                resolve();
            }
        });
    }

    /*
    * Hide the modal
    * */
    hideModal(delayAfter) {
        return new Promise((resolve => {
            this.$modalCard.classList.add("modal-hidden");
            if (delayAfter === true) {
                setTimeout(() => {
                    resolve();
                }, 500);
            } else {
                resolve();
            }
        }))
    }

    /*
    * ScoreList should be sorted
    * [{
    *   playerIndex: int,
    *   score: int
    * }]
    * */
    showScoreboard(scoreList) {
        let scoreboardTemplate = `<div id="scoreboard">`;
        for (let index in scoreList) {
            let rank = parseInt(index) + 1;
            scoreboardTemplate += `
                <div class="scoreboard-row">
                    <span class="scoreboard-ranking">${rank}</span>
                    <img class="chat-message-avatar" src="${this.players[scoreList[index].playerIndex].avatar}">
                    <span class="scoreboard-username">${this.players[scoreList[index].playerIndex].fullName}</span>
                    <div class="monopoly-cash">M</div>
                    <span class="scoreboard-score">${scoreList[index].score}</span>
                </div>`;
        }
        scoreboardTemplate += "</div>";
        this.$modalCardContent.classList.add("scoreboard-bg");
        this.showModal(null, "Scoreboard", "Good Game!", scoreboardTemplate, [{
            text: "Start a New Game",
            callback: () => {
                window.location = `http://${window.location.host}/monopoly/join`;
            }
        }]);
    }


    showHelp() {
        this.showingHelp = !this.showingHelp;

        if (this.showingHelp) {
            this.$helpControl.classList.remove("control-off");
            this.$helpOverlay.classList.remove("hidden");
        } else {
            this.$helpControl.classList.add("control-off");
            this.$helpOverlay.classList.add("hidden");
        }
    }

}

window.onload = () => {
    new GameView();
};

GameView.DEFAULT_AVATAR = "/static/images/favicon.png";

GameView.PLAYERS_COLORS = ["#FFD54F", "#90CAF9", "#E0E0E0", "#B39DDB"];