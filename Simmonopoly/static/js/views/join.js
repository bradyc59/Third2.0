class Join {
    constructor() {
        this.userName = document.getElementById("user-name").value;
        this.roomName = document.getElementById("room_code").value;

        this.initComponents();
        this.initWebsockets();
    }

    initComponents() {
        this.$userContainer = document.getElementById("joined-users-container");
        const isProfileInited = document.getElementById("user-avatar").getAttribute("src").length !== 0;
        if (!isProfileInited) {
            const $addProfileButton = document.getElementById("init-profile");
            $addProfileButton.classList.remove("hidden");
        }
    }

    initWebsockets() {
        const connectionString = 'ws://' + window.location.host + '/ws/join/' + this.roomName + '/';
        const gameSocket = new WebSocket(connectionString);
        gameSocket.onopen = function open() {
            console.log('WebSockets connection created.');
            gameSocket.send(JSON.stringify({
                "event": "START",
                "message": ""
            }));
        };

        gameSocket.onclose = function (e) {
            console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
            setTimeout(function () {
                this.initWebsockets();
            }, 1000);
        };

        if (gameSocket.readyState == WebSocket.OPEN) {
            gameSocket.onopen();
        }
    }
    handleStatusChange(message) {
        if (message.action === "join") {
            this.addFriend(message.data);

            if (this.friends.length > 1) {
                if (this.hostName !== this.userName) {
                    this.$startGame.innerText = "Waiting for host to start the game...";
                } else {
                    this.$startGame.disabled = false;
                    this.$startGame.innerText = "Start Game";
                }
            }
        } else if (message.action === "start") {
            this.navigateToGame();
        } else if (message.action === "fail_join") {
            this.$startGame.disabled = true;
            this.$startGame.innerText = "Navigating back... Create your own game!";
            this.$newGameNotice.innerText = "4 Players Max Per Game!";
            this.$newGameNotice.style.color = "#F44336";
            setTimeout(this.navigateBack, 2000);
        }
    }
}
window.onload = () => {
    new Join();
};





