const video = document.querySelector('video')
const img = document.getElementById('frame')
const URL = `ws://${window.location.host}/ws/socket-server/`
const RECOGNITION_FPS = 2
const CAMERA_FPS = 60
const CameraSocket = new WebSocket(URL)

let x = 0, y = 0, w = 0, h = 0, emotion = ''
let faces = []

// request access to webcam
navigator.mediaDevices.getUserMedia({
    video: {
        width: 426,
        height: 240
    }
}).then((stream) => video.srcObject = stream).catch(
    // throw new Error("Something went badly wrong!")
)

const getFrame = (isClear = false) => {
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext('2d')

    ctx.drawImage(video, 0, 0);
    if (isClear) {
        return canvas.toDataURL('image/png')
    }

    if (faces.length) {
        ctx.font = "48px serif";
        ctx.fillStyle = "rgb(0,250,154)"
        ctx.strokeStyle = "rgb(0,250,154)"
        faces.forEach((face => {
            ctx.strokeRect(face.x, face.y, face.w, face.h)
            ctx.fillText(face.emotion, face.x, face.y)
        }))
    }

    return canvas.toDataURL('image/png')
}


CameraSocket.onopen = () => {
    console.log(`Connected to ${URL}`);
    setInterval(() => {
        CameraSocket.send(JSON.stringify({
            'frame': getFrame(true)

        }))
    }, 1000 / RECOGNITION_FPS)

    setInterval(() => {
        let frame = getFrame()
        if (frame.length > 6) {
            img.src = frame
        }

    }, 1000 / CAMERA_FPS)
}

CameraSocket.onmessage = message => {
    let data = JSON.parse(message.data)
    if (data.type === 'classifier') {
        img.src = getFrame()

        let result = data.result

        if (result == null) {
            faces = []
            return
        }
        faces = result
    }
}
