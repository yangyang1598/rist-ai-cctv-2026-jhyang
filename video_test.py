import os
import time
import cv2

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

def main():
    rtsp_url = "rtsp://localhost:8554/05"
    print(f"🔗 [{rtsp_url}] 연결 시도 중 (하드웨어 가속 디코딩)...")

    try:
        params = cv2.cudacodec.VideoReaderInitParams()
        params.udpSource = True
        params.allowFrameDrop = True
        gpu_reader = cv2.cudacodec.createVideoReader(rtsp_url, params=params)
        print("✅ RTSP 스트림에 성공적으로 연결되었습니다!")
    except Exception as e:
        try:
            cap = cv2.VideoCapture(rtsp_url)
            if not cap.isOpened():
                raise Exception("FFMPEG로도 연결 실패")
            print("✅ FFMPEG로 RTSP 스트림에 연결되었습니다! (하드웨어 가속 실패, CPU 디코딩으로 fallback)")
            return
        
        except Exception as e2:
            print(f"❌ FFMPEG로도 연결 실패: {e2}")
            return

    try:
        while True:
            ret, gpu_frame = gpu_reader.nextFrame()
            if not ret or gpu_frame.empty():
                print("⚠️ 스트림 끊김")
                break

            frame = gpu_frame.download()

            cv2.imshow("RTSP Stream (GPU Decoding)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("⏹️ 스트림 처리 중단")
                break

    except KeyboardInterrupt as e:
        print("⏹️ 스트림 처리 중단")
    
    except Exception as e:
        print(f"❌ 스트림 처리 중 오류 발생: {e}")

    finally:
        del gpu_reader

if __name__ == "__main__":
    main()