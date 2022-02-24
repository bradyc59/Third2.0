document.querySelector('#room_code').focus();
        document.querySelector('#room_code').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#submit').click();
            }
        };
