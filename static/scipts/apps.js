const root = document.getElementById('root');
const usernameInput = document.getElementById('username');
const button = document.getElementById('join_leave');
const shareScreen = document.getElementById('share_screen');
const toggleChat = document.getElementById('toggle_chat');
const container = document.getElementById('container');
const count = document.getElementById('count');
const chatScroll = document.getElementById('chat-scroll');
const chatContent = document.getElementById('chat-content');
const chatInput = document.getElementById('chat-input');
let connected = false;
let room;
let chat;
let conv;
let screenTrack;

function addLocalVideo() {
  console.log("hiiiiiiiiiiiii");
  alert('addLocalVideo');
  Twilio.Video.createLocalVideoTrack().then(track => {
    let video = document.getElementById('local').firstChild;
    alert(video);
    let trackElement = track.attach();
    // alert("I am showing name!");
    container.append(track.attach());

    trackElement.addEventListener('click', () => {
      zoomTrack(trackElement);
    });
    video.appendChild(trackElement);
  });
};
//
// function addLocalVideo() {
//   alert("Add participant na");
//   Twilio.Video.createLocalVideoTrack().then(track => {
//     let video = document.getElementById('local').firstChild;
//     video.appendChild(track.attach());
//   });
// };

function connectButtonHandler(event) {
  event.preventDefault();
  if (!connected) {
    let username = usernameInput.value;
    if (!username) {
      alert('Enter your name before connecting');
      return;
    }
    button.disabled = true;
    button.innerHTML = 'Connecting...';
    alert(username);
    connect(username).then(() => {
      button.innerHTML = 'Leave call';
      button.disabled = false;
      shareScreen.disabled = false;
    }).catch(() => {
      alert('Connection failed. Is the backend running?');
      button.innerHTML = 'Join call';
      button.disabled = false;
    });
  } else {
    disconnect();
    button.innerHTML = 'Join call';
    connected = false;
    shareScreen.innerHTML = 'Share screen';
    shareScreen.disabled = true;
  }
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function connect(username) {
  alert('connect');
  let promise = new Promise((resolve, reject) => {
    // get a token from the back end
    let data;
    // alert("before append")
    const csrftoken = getCookie('csrftoken');
    // data.append('csrfmiddlewaretoken', $('#csrf-helper input[name="csrfmiddlewaretoken"]').attr('value')); ,{headers: {'X-CSRFToken': csrftoken}}
    // alert("change12")
    const request = new Request('/videocall/');
    // alert(request.url)
    fetch(request, {
      method: 'POST',
      // headers: {
      //     "X-CSRFToken": getCookie("csrftoken"),
      //     "Accept": "application/json",
      //     "Content-Type": "application/json"
      // },
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        'X-CSRFToken': csrftoken,
      },
      // credentials: 'include'
      credentials: "same-origin",
      body: JSON.stringify({
        'username': username
      })
    }).then(res => res.json()).then(_data => {
      // join video call
      // alert("Joint")
      data = _data;
      return Twilio.Video.connect(data.token);
    }).then(_room => {
      // alert("room")
      room = _room;
      room.participants.forEach(participantConnected);
      room.on('participantConnected', participantConnected);
      room.on('participantDisconnected', participantDisconnected);
      connected = true;
      updateParticipantCount();
      connectChat(data.token, data.conversation_sid);
      resolve();
    }).catch(e => {
      // alert("catch")
      console.log(e);
      reject();
    });
    // alert(promise)

  });
  return promise;
};



function updateParticipantCount() {
  if (!connected)
    count.innerHTML = 'Disconnected.';
  else
    count.innerHTML = (room.participants.size + 1) + ' participants online.';
};

function participantConnected(participant) {
  let participantDiv = document.createElement('div');
  participantDiv.setAttribute('id', participant.sid);
  participantDiv.setAttribute('class', 'participant');

  let tracksDiv = document.createElement('div');
  participantDiv.appendChild(tracksDiv);

  let labelDiv = document.createElement('div');
  labelDiv.setAttribute('class', 'label');
  labelDiv.innerHTML = participant.identity;
  participantDiv.appendChild(labelDiv);

  container.appendChild(participantDiv);

  participant.tracks.forEach(publication => {
    if (publication.isSubscribed)
      trackSubscribed(tracksDiv, publication.track);
  });
  participant.on('trackSubscribed', track => trackSubscribed(tracksDiv, track));
  participant.on('trackUnsubscribed', trackUnsubscribed);

  updateParticipantCount();
};

function participantDisconnected(participant) {
  document.getElementById(participant.sid).remove();
  updateParticipantCount();
};

function trackSubscribed(div, track) {
  let trackElement = track.attach();
  trackElement.addEventListener('click', () => {
    zoomTrack(trackElement);
  });
  div.appendChild(trackElement);
};

function trackUnsubscribed(track) {
  track.detach().forEach(element => {
    if (element.classList.contains('participantZoomed')) {
      zoomTrack(element);
    }
    element.remove()
  });
};

function disconnect() {
  room.disconnect();
  if (chat) {
    chat.shutdown().then(() => {
      conv = null;
      chat = null;
    });
  }
  while (container.lastChild.id != 'local')
    container.removeChild(container.lastChild);
  button.innerHTML = 'Join call';
  if (root.classList.contains('withChat')) {
    root.classList.remove('withChat');
  }
  toggleChat.disabled = true;
  connected = false;
  updateParticipantCount();
};

function shareScreenHandler() {
  event.preventDefault();
  if (!screenTrack) {
    navigator.mediaDevices.getDisplayMedia().then(stream => {
      screenTrack = new Twilio.Video.LocalVideoTrack(stream.getTracks()[0]);
      room.localParticipant.publishTrack(screenTrack);
      screenTrack.mediaStreamTrack.onended = () => {
        shareScreenHandler()
      };
      console.log(screenTrack);
      shareScreen.innerHTML = 'Stop sharing';
    }).catch(() => {
      alert('Could not share the screen.')
    });
  } else {
    room.localParticipant.unpublishTrack(screenTrack);
    screenTrack.stop();
    screenTrack = null;
    shareScreen.innerHTML = 'Share screen';
  }
};

function zoomTrack(trackElement) {
  if (!trackElement.classList.contains('trackZoomed')) {
    // zoom in
    container.childNodes.forEach(participant => {
      if (participant.classList && participant.classList.contains('participant')) {
        let zoomed = false;
        participant.childNodes[0].childNodes.forEach(track => {
          if (track === trackElement) {
            track.classList.add('trackZoomed')
            zoomed = true;
          }
        });
        if (zoomed) {
          participant.classList.add('participantZoomed');
        } else {
          participant.classList.add('participantHidden');
        }
      }
    });
  } else {
    // zoom out
    container.childNodes.forEach(participant => {
      if (participant.classList && participant.classList.contains('participant')) {
        participant.childNodes[0].childNodes.forEach(track => {
          if (track === trackElement) {
            track.classList.remove('trackZoomed');
          }
        });
        participant.classList.remove('participantZoomed')
        participant.classList.remove('participantHidden')
      }
    });
  }
};

function connectChat(token, conversationSid) {
  return Twilio.Conversations.Client.create(token).then(_chat => {
    chat = _chat;
    return chat.getConversationBySid(conversationSid).then((_conv) => {
      conv = _conv;
      conv.on('messageAdded', (message) => {
        addMessageToChat(message.author, message.body);
      });
      return conv.getMessages().then((messages) => {
        chatContent.innerHTML = '';
        for (let i = 0; i < messages.items.length; i++) {
          addMessageToChat(messages.items[i].author, messages.items[i].body);
        }
        toggleChat.disabled = false;
      });
    });
  }).catch(e => {
    console.log(e);
  });
};

function addMessageToChat(user, message) {
  chatContent.innerHTML += `<p><b>${user}</b>: ${message}`;
  chatScroll.scrollTop = chatScroll.scrollHeight;
}

function toggleChatHandler() {
  event.preventDefault();
  if (root.classList.contains('withChat')) {
    root.classList.remove('withChat');
  } else {
    root.classList.add('withChat');
    chatScroll.scrollTop = chatScroll.scrollHeight;
  }
};

function onChatInputKey(ev) {
  if (ev.keyCode == 13) {
    conv.sendMessage(chatInput.value);
    chatInput.value = '';
  }
};
// alert('pata ha');
// console.log("Aya");
// addLocalVideo();
// alert("changed");

button.addEventListener('click', connectButtonHandler);
shareScreen.addEventListener('click', shareScreenHandler);
toggleChat.addEventListener('click', toggleChatHandler);
chatInput.addEventListener('keyup', onChatInputKey);
