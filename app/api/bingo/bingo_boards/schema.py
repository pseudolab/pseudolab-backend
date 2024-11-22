from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from core.base_schema import BaseSchema
from models.bingo.schema import BingoEventUserInfo


class BingoBoardRequest(BaseModel):
    user_id: int = Field(..., title="유저 ID")
    board_data: dict = Field(..., title="빙고판 데이터")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "board_data": {
                    "0": {"value": "AI 스타트업 재직자", "selected": 1, "status": 1},
                    "1": {"value": "AI 아티스트", "selected": 1, "status": 0},
                    "2": {"value": "AI 뉴스레터 구독자", "selected": 1, "status": 0},
                    "3": {"value": "AI 유튜브 채널 구독자", "selected": 0, "status": 0},
                    "4": {"value": "프론트엔드, 백엔드 엔지니어", "selected": 0, "status": 1},
                    "5": {"value": "오픈소스 기여자", "selected": 0, "status": 0},
                    "6": {"value": "SNS 사용자", "selected": 0, "status": 0},
                    "7": {"value": "직전 경력 특이한", "selected": 0, "status": 1},
                    "8": {"value": "AI 모델 배포 경험자", "selected": 0, "status": 0},
                    "9": {"value": "기술 블로그 운영자", "selected": 0, "status": 0},
                    "10": {"value": "해외 컨퍼런스 참가경험", "selected": 0, "status": 0},
                    "11": {"value": "귀여운 IT 굿즈 받아본자", "selected": 0, "status": 0},
                    "12": {"value": "Welcome to PseudoCon", "selected": 0, "status": 0},
                    "13": {"value": "부트캠프 참가경험", "selected": 0, "status": 0},
                    "14": {"value": "AI 관련 해커톤 경험자", "selected": 0, "status": 0},
                    "15": {"value": "올해를 알차게 보낸자", "selected": 0, "status": 0},
                    "16": {"value": "AI 윤리/정책 연구자", "selected": 0, "status": 0},
                    "17": {"value": "로봇/드론 관련 연구자", "selected": 0, "status": 0},
                    "18": {"value": "내 MBTI 설명 가능한자", "selected": 0, "status": 0},
                    "19": {"value": "VR/AR 헤드셋 보유자", "selected": 0, "status": 0},
                    "20": {"value": "Kaggle 또는 Dacon 우승자", "selected": 0, "status": 0},
                    "21": {"value": "멀티모달 관련 연구자", "selected": 0, "status": 0},
                    "22": {"value": "특별한 경험을 가진자", "selected": 0, "status": 0},
                    "23": {"value": "DevOps, MLOps, SRE", "selected": 0, "status": 0},
                    "24": {"value": "이전 기수 참가자", "selected": 0, "status": 0},
                },
            }
        }


class BingoBoardResponse(BaseSchema):
    user_id: Optional[int] = Field(title="유저 ID", default=None)
    board_data: Optional[dict] = Field(title="빙고판 데이터", default=None)
    bingo_count: Optional[int] = Field(title="빙고 갯수", default=None)
    created_at: Optional[datetime] = Field(title="생성일", default=None)
    updated_at: Optional[datetime] = Field(title="수정일", default=None)


class UpdateBingoCountResponse(BaseSchema):
    user_id: Optional[int] = Field(title="유저 ID", default=None)
    bingo_count: Optional[int] = Field(title="업데이트된 빙고 갯수", default=None)


class UserSelectedWordsResponse(BaseSchema):
    selected_words: Optional[list[str]] = Field(title="선택한 단어들", default=None)


class UpdateBingoStatusResponse(BaseSchema):
    send_user_id: Optional[int] = Field(title="요청 유저 ID", default=None)
    receive_user_id: Optional[int] = Field(title="대상 유저 ID", default=None)
    updated_words: Optional[list[str]] = Field(title="업데이트된 단어들", default=None)
    bingo_count: Optional[int] = Field(title="업데이트된 빙고 갯수", default=None)


class UpdateBingoStatusResponseByQRScan(UpdateBingoCountResponse):
    booth_id: Optional[int] = Field(title="요청 부스 ID", default=None)
    updated_words: Optional[list[str]] = Field(title="업데이트된 단어들", default=None)


class GetUserBingoEventUser(BaseSchema):
    bingo_event_users: Optional[list[BingoEventUserInfo]] = Field(title="빙고 이벤트 당첨 유저 목록", default=None)
