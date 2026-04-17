
# 이메일 설정
RPA_EMAIL_SMTP_SERVER = 'smtp.gmail.com'
RPA_EMAIL_SMTP_PORT = 587
RPA_EMAIL_ADDRESS = 'mymail072332@gmail.com'
RPA_EMAIL_APP_PASSWORD = 'gbbc odpf ndne mabk'  # 앱 비밀번호

# 보안 설정
RPA_TLS_ENABLED = True

# 스케줄링 설정
RPA_SCHEDULE_INTERVAL_SEC = 1  # 스케줄 반복 확인 간격 (초)

# 첨부파일 관련 설정
RPA_ATTACHMENT_MAX_SIZE_MB = 25
RPA_ATTACHMENT_ALLOWED_EXTENSIONS = ['pdf', 'docx', 'xlsx', 'png', 'jpg']
RPA_DEFAULT_ATTACHMENT_DIR = './attachments'

# 로그 설정
RPA_LOG_FILE = './logs/email_scheduler.log'
RPA_LOG_LEVEL = 'INFO'