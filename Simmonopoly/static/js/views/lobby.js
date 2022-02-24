document.querySelector('#room_code').focus();
        document.querySelector('#room_code').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#submit').click();
            }
        };

        document.querySelector('#room-name-submit').onclick = function(e) {
            var roomName = document.querySelector('#room-name-input').value;
            window.location.pathname = '/join/' + roomName + '/';
        };