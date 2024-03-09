const APP_ID = '02f11f6818554a19a162e482329511b4';
const TOKEN = sessionStorage.getItem('token');
const CHANNEL = sessionStorage.getItem('room');
let UID = sessionStorage.getItem('UID');

let NAME = sessionStorage.getItem('name');

const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' });

let localTracks = [];
let remoteUsers = {};

let irisDetectionInterval;  // Variable to store the interval ID for iris detection
let mediaRecorder;


console.log(CHANNEL)
const roomIDInput = '12345'


let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL;

    client.on('user-published', handleUserJoined);
    client.on('user-left', handleUserLeft);

    try {
        UID = await client.join(APP_ID, CHANNEL, TOKEN, UID);
    } catch (error) {
        console.error(error);
        window.open('/', '_self');
    }

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks();
    // Ensure localTracks is an array with at least two elements
    if (localTracks && localTracks.length >= 2) {
        // Access the MediaStream property of the second element (index 1)
        const mediaStream = localTracks[1].mediaStream;

        // Check if mediaStream is a valid MediaStream object
        if (mediaStream instanceof MediaStream) {
            console.log('MediaStream is valid:', mediaStream);
        } else {
            console.error('localTracks[1].mediaStream is not a valid MediaStream object.');
        }

        // Rest of your code...
        let member = await createMember();

        let player = `<div  class="video-container" id="user-container-${UID}">
                        <div class="video-player" id="user-${UID}"></div>
                        <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                    </div>`;

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player);
        localTracks[1].play(`user-${UID}`);
        await client.publish([localTracks[0], localTracks[1]]);
    } else {
        console.error('Error: localTracks array is not properly initialized.');
    }

    
};

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user;
    await client.subscribe(user, mediaType);

    if (mediaType === 'video') {
        let player = document.getElementById(`user-container-${user.uid}`);
        if (player != null) {
            player.remove();
        }

        let member = await getMember(user);

        player = `<div  class="video-container" id="user-container-${user.uid}">
            <div class="video-player" id="user-${user.uid}"></div>
            <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
        </div>`;

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player);
        user.videoTrack.play(`user-${user.uid}`);
    }

    if (mediaType === 'audio') {
        user.audioTrack.play();
    }
};

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid];
    document.getElementById(`user-container-${user.uid}`).remove();
};

let leaveAndRemoveLocalStream = async () => {
    for (let i = 0; localTracks.length > i; i++) {
        localTracks[i].stop();
        localTracks[i].close();
    }

    await client.leave();
    // This is somewhat of an issue because if the user leaves without actually pressing the leave button, it will not trigger
    deleteMember();
    clearInterval(irisDetectionInterval);  // Stop iris detection when leaving
    window.open('/', '_self');
};

let toggleCamera = async (e) => {
    console.log('TOGGLE CAMERA TRIGGERED');
    if (localTracks[1].muted) {
        await localTracks[1].setMuted(false);
        e.target.style.backgroundColor = '#fff';
    } else {
        await localTracks[1].setMuted(true);
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)';
    }
};

let toggleMic = async (e) => {
    console.log('TOGGLE MIC TRIGGERED');
    if (localTracks[0].muted) {
        await localTracks[0].setMuted(false);
        e.target.style.backgroundColor = '#fff';
    } else {
        await localTracks[0].setMuted(true);
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)';
    }
};

let createMember = async () => {
    let response = await fetch('/create_member/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'name': NAME, 'room_name': CHANNEL, 'UID': UID }),
    });
    let member = await response.json();
    return member;
};

let getMember = async (user) => {
    let response = await fetch(`/get_member/?UID=${user.uid}&room_name=${CHANNEL}`);
    let member = await response.json();
    return member;
};

let deleteMember = async () => {
    let response = await fetch('/delete_member/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'name': NAME, 'room_name': CHANNEL, 'UID': UID }),
    });
    let member = await response.json();
};

// let startIrisDetection = async () => {
//     console.log('Starting iris detection...');

//     const streamConfig = { video: true, audio: true };
//     const localStream = await navigator.mediaDevices.getUserMedia(streamConfig);

//     mediaRecorder = new MediaRecorder(localStream);
//     mediaRecorder.ondataavailable = async (event) => {
//         if (event.data.size > 0) {
//             const buffer = await event.data.arrayBuffer();

//             // Process the buffer or send it directly to the backend
//             // Modify this part based on your requirements
//             console.log(buffer)
//             socket.send(buffer);
//         }
//     };
//     mediaRecorder.start(1000);
// };
let startIrisDetection = async () => {
    console.log('Starting iris detection...');

    // Access the video track from Agora's local stream
    const agoraVideoTrack = localTracks[1];
    
    // Get the MediaStream from Agora's video track
    const agoraMediaStream = agoraVideoTrack.mediaStream;

    // Create a new MediaRecorder for Agora's video stream
    mediaRecorder = new MediaRecorder(agoraMediaStream);

    mediaRecorder.ondataavailable = async (event) => {
        if (event.data.size > 0) {
            const buffer = await event.data.arrayBuffer();

            // Process the buffer or send it directly to the backend
            // Modify this part based on your requirements
            console.log(buffer)
            socket.send(buffer);
        }
    };

    mediaRecorder.start(1000);
};




let stopIrisDetection = () => {
    clearInterval(irisDetectionInterval);
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
};

// Function to send Agora signaling messages
function sendAgoraSignal(message) {
    socket.send(JSON.stringify({ type: 'agora_signal', message: message }));
}
// Function to handle Agora signaling messages
function handleAgoraSignal(data) {
    // Implement your Agora signaling logic here
    console.log('Agora signaling message:', data.message);
}

// Function to send video frames for iris detection
// function sendFrameToBackend(videoFrame) {
//     const mediaRecorder = new MediaRecorder(videoFrame);
//     mediaRecorder.ondataavailable = async (event) => {
//         if (event.data.size > 0) {
//             // Convert Blob to ArrayBuffer
//             const buffer = await event.data.arrayBuffer();
            
//             // Send the buffer to the backend using WebSocket
//             socket.send(buffer);
//             socket.send(JSON.stringify({ type: 'iris_detection_frame', frame: videoFrame }));
//         }
//     };
//     mediaRecorder.start(1000);
// }

// Function to handle iris detection result
function handleIrisDetectionResult(data) {
    // Implement logic to update UI based on iris detection result
    console.log('Iris Detection Result:', data.result);

    // For example, show a red color popup on the user's screen
    const redPopup = document.createElement('div');
    redPopup.style.backgroundColor = 'red';
    redPopup.style.position = 'fixed';
    redPopup.style.top = '50%';
    redPopup.style.left = '50%';
    redPopup.style.transform = 'translate(-50%, -50%)';
    redPopup.style.padding = '20px';
    redPopup.innerText = 'Iris Detected!';

    document.body.appendChild(redPopup);
}

window.addEventListener("beforeunload", deleteMember);

joinAndDisplayLocalStream();
// Continue with your existing event listeners
document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream);
document.getElementById('camera-btn').addEventListener('click', toggleCamera);
document.getElementById('mic-btn').addEventListener('click', toggleMic);


const socket = new WebSocket(`ws://${window.location.host}/ws/call/${roomIDInput}/`);
socket.addEventListener('open', () => {
    console.log('WebSocket connected');
    socket.send(
        JSON.stringify({
            command: "join_room",      // join room command
            room: CHANNEL,
          })
    )
});
socket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);

    // Check the type of message (Agora signaling, iris detection frame, or result)
    if (data.type === 'agora_signal') {
        // Handle Agora signaling messages
        handleAgoraSignal(data);
    } else if (data.type === 'iris_detection_result') {
        // Handle iris detection result
        handleIrisDetectionResult(data);
    }
    else if(data.type=='joined'){
        console.log(data.text)
    }
});
socket.addEventListener('close', () => {
    console.log('WebSocket closed');
});

// Event listener for the button click to start iris detection
document.getElementById('startIrisDetection').addEventListener('click', startIrisDetection);
// Event listener to stop iris detection when another button is clicked
document.getElementById('stopIrisDetection').addEventListener('click', stopIrisDetection);
// background removel 
document.getElementById('startBackgroundRemoval').addEventListener('click', () => {
    // Communicate with the server to initiate background removal
    socket.send(JSON.stringify({ type: 'start_background_removal' }));
});