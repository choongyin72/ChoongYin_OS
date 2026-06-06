"""
Keep-Alive Script — prevents Windows screen lock during deep dive sessions.
Moves mouse 1 pixel every 4 minutes to simulate activity.
Run this BEFORE leaving the PC for deep dive sessions.
Stop it manually (Ctrl+C) after all sessions complete.
"""
import ctypes, time, sys
from datetime import datetime

INTERVAL = 60   # 1 minute — well under any corporate lock timeout
MOVE_PX  = 1    # pixels to move (invisible to user)

def get_cursor_pos():
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def jiggle():
    x, y = get_cursor_pos()
    ctypes.windll.user32.SetCursorPos(x + MOVE_PX, y)
    time.sleep(0.1)
    ctypes.windll.user32.SetCursorPos(x, y)  # move back

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}', flush=True)

if __name__ == '__main__':
    log('Keep-alive started. Mouse will jiggle every 1 minute to prevent screen lock.')
    log('Press Ctrl+C to stop.')
    log('Sessions scheduled: D=09:11, E=11:41, F=14:41, G=17:11, H=20:41, I=23:11')
    log('Next day: ET-A=02:11, ET-B=05:11, ET-C=08:11, ET-D=10:41, ET-E=13:41')
    log('')

    count = 0
    try:
        while True:
            time.sleep(INTERVAL)
            count += 1
            jiggle()
            log(f'Jiggle #{count} — keeping screen active')
    except KeyboardInterrupt:
        log('Keep-alive stopped.')
        sys.exit(0)
