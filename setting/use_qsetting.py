import os
import configparser
from typing import Any, Dict, List, Optional

class Setting:
    def __init__(self, ini_file=None):
        home_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_dir = os.path.join(home_dir, "config")
        os.makedirs(config_dir, exist_ok=True)
        if ini_file:
            self.settings_file = os.path.join(config_dir, ini_file)
        else:
            self.settings_file = os.path.join(config_dir, "CameraManager.ini")

        self.config = configparser.ConfigParser(inline_comment_prefixes=(";",))
        # UTF-8 인코딩으로 파일 읽기
        if os.path.exists(self.settings_file):
            self.config.read(self.settings_file, encoding='utf-8')
    
    def get(self, key, defaultValue=None, group=None):
        """설정 값을 가져옵니다."""
        try:
            if group:
                return self.config.get(group, key)
            else:
                # group이 없을 때는 모든 섹션에서 키를 찾습니다
                # 먼저 DEFAULT 섹션에서 찾기
                if key in self.config.defaults():
                    return self.config.defaults()[key]
                
                # 모든 섹션에서 키 찾기
                for section_name in self.config.sections():
                    if self.config.has_option(section_name, key):
                        return self.config.get(section_name, key)
                
                # 찾지 못한 경우 기본값 반환
                print(f"get: {key} not found, returning default value")
                return defaultValue
            
        except (configparser.NoSectionError, configparser.NoOptionError):
            return defaultValue
    
    def set(self, key, value, group=None):
        """설정 값을 저장합니다."""
        if group:
            if not self.config.has_section(group):
                self.config.add_section(group)
            self.config.set(group, key, str(value))
        else:
            self.config.set('DEFAULT', key, str(value))
        
        # UTF-8 인코딩으로 파일 저장
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get_all_keys(self, group=None):
        """특정 그룹의 모든 키를 가져옵니다."""
        try:
            if group:
                if self.config.has_section(group):
                    return list(self.config.options(group))
                else:
                    return []
            else:
                return list(self.config.defaults().keys())
        except Exception:
            return []
    
    #region 2025-07-09: 글로벌 설정용 딕셔너리화 메소드 추가
    def get_all_groups(self) -> List[str]:
        """모든 그룹 이름을 반환합니다."""
        try:
            return self.config.sections()
        except Exception as e:
            print(f"Failed to get groups: {e}")
            return []
    
    def to_dict(self, group: Optional[str] = None, include_global: bool = True) -> Dict[str, Any]:
        """
        설정을 딕셔너리로 반환합니다.
        """
        try:
            if group is not None:
                # 특정 그룹만 반환
                return self._get_group_dict(group)
            else:
                # 전체 구조 반환
                return self._get_full_structure(include_global)
        except Exception as e:
            print(f"Failed to generate dict for group '{group}': {e}")
            return {}
        
    def _get_group_dict(self, group: str) -> Dict[str, Any]:
        """특정 그룹의 설정을 딕셔너리로 반환합니다."""
        if not self.config.has_section(group):
            return {}
        return dict(self.config.items(group))

    def _get_full_structure(self, include_global: bool = True) -> Dict[str, Dict[str, Any]]:
        """전체 INI 구조를 중첩 딕셔너리로 반환합니다."""
        result = {}
        
        # 글로벌 설정 (그룹 없는 최상위 설정)
        if include_global:
            defaults = dict(self.config.defaults())
            if defaults:
                result["global"] = defaults
        
        # 각 그룹별 설정
        groups = self.get_all_groups()
        for group in groups:
            group_dict = self._get_group_dict(group)
            if group_dict:  # 빈 그룹은 제외
                result[group] = group_dict
        
        return result
    #endregion
    
    def reload(self):
        """설정 파일을 다시 읽어옵니다."""
        if os.path.exists(self.settings_file):
            self.config.read(self.settings_file, encoding='utf-8')