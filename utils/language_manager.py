"""
Enhanced Language Manager for multi-language test automation
Provides comprehensive language switching, text management, and validation
"""

import logging
from contextlib import contextmanager
from typing import Dict, List, Optional, Any, Set
import importlib
import os


class LanguageManager:
    """
    Enhanced Language Manager with comprehensive multi-language support
    """
    
    # Supported language mappings
    LANGUAGE_MAPPINGS = {
        'en': 'en',
        'english': 'en', 
        'vi': 'vi',
        'vietnamese': 'vi',
        'vn': 'vi'
    }
    
    # Language display names
    LANGUAGE_NAMES = {
        'en': 'English',
        'vi': 'Tiếng Việt'
    }
    
    def __init__(self, default_language: str = 'en'):
        """
        Initialize Language Manager
        
        Args:
            default_language: Default language code ('en', 'vi', etc.)
        """
        self.logger = logging.getLogger(__name__)
        self.current_language = self._normalize_language_code(default_language)
        self.default_language = self.current_language
        self.language_data = {}
        self._load_all_languages()
        
        self.logger.info(f"LanguageManager initialized with default language: {self.current_language}")
    
    def _normalize_language_code(self, language: str) -> str:
        """
        Normalize language code to standard format
        
        Args:
            language: Language code or name
            
        Returns:
            Normalized language code
        """
        if not language:
            return 'en'
            
        normalized = language.lower().strip()
        return self.LANGUAGE_MAPPINGS.get(normalized, 'en')
    
    def _load_all_languages(self):
        """Load language data for all supported languages"""
        for lang_code in self.LANGUAGE_MAPPINGS.values():
            if lang_code not in self.language_data:
                self._load_language_data(lang_code)
    
    def _load_language_data(self, language_code: str):
        """
        Load language data from expectations/languages files
        
        Args:
            language_code: Language code to load
        """
        try:
            # Map language codes to module names
            module_map = {
                'en': 'english',
                'vi': 'vietnamese'
            }
            
            module_name = module_map.get(language_code, 'english')
            module_path = f'expectations.languages.{module_name}'
            
            # Import the language module
            language_module = importlib.import_module(module_path)
            
            # Extract language data
            language_data = {}
            for attr_name in dir(language_module):
                if not attr_name.startswith('_'):
                    attr_value = getattr(language_module, attr_name)
                    if isinstance(attr_value, dict):
                        language_data[attr_name.lower()] = attr_value
            
            self.language_data[language_code] = language_data
            self.logger.info(f"Loaded language data for: {language_code}")
            
        except ImportError as e:
            self.logger.warning(f"Could not load language data for {language_code}: {e}")
            # Create empty language data as fallback
            self.language_data[language_code] = {
                'messages': {},
                'button_texts': {},
                'labels': {},
                'validation_messages': {}
            }
        except Exception as e:
            self.logger.error(f"Error loading language data for {language_code}: {e}")
            self.language_data[language_code] = {}
    
    def set_language(self, language: str):
        """
        Set current language
        
        Args:
            language: Language code or name
        """
        normalized_lang = self._normalize_language_code(language)
        
        if normalized_lang not in self.language_data:
            self._load_language_data(normalized_lang)
        
        self.current_language = normalized_lang
        self.logger.info(f"Language switched to: {normalized_lang}")
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        return list(set(self.LANGUAGE_MAPPINGS.values()))
    
    def get_current_language_info(self) -> Dict[str, str]:
        """Get current language information"""
        return {
            'code': self.current_language,
            'name': self.LANGUAGE_NAMES.get(self.current_language, 'Unknown'),
            'available_categories': list(self.language_data.get(self.current_language, {}).keys())
        }
    
    def get_text_by_category(self, category: str, key: str, fallback: bool = True) -> str:
        """
        Get text by category and key
        
        Args:
            category: Text category ('messages', 'button_texts', etc.)
            key: Text key
            fallback: Whether to use fallback mechanisms
            
        Returns:
            Text in current language
        """
        # Try current language first
        current_data = self.language_data.get(self.current_language, {})
        category_data = current_data.get(category.lower(), {})
        
        if key in category_data:
            return category_data[key]
        
        if not fallback:
            return f"[Missing: {key}]"
        
        # Fallback to other languages
        for lang_code in self.get_supported_languages():
            if lang_code != self.current_language:
                lang_data = self.language_data.get(lang_code, {})
                category_data = lang_data.get(category.lower(), {})
                if key in category_data:
                    self.logger.warning(f"Using fallback text for {key} from {lang_code}")
                    return category_data[key]
        
        # Final fallback
        return f"[Missing: {key}]"
    
    def get_message(self, key: str, fallback: bool = True) -> str:
        """Get message text"""
        return self.get_text_by_category('messages', key, fallback)
    
    def get_button_text(self, key: str, fallback: bool = True) -> str:
        """Get button text"""
        return self.get_text_by_category('button_texts', key, fallback)
    
    def get_label_text(self, key: str, fallback: bool = True) -> str:
        """Get label text"""
        return self.get_text_by_category('labels', key, fallback)
    
    def get_validation_message(self, key: str, fallback: bool = True) -> str:
        """Get validation message"""
        return self.get_text_by_category('validation_messages', key, fallback)
    
    def bulk_get_texts(self, keys: List[str], category: str = 'messages') -> Dict[str, str]:
        """
        Get multiple texts at once for better performance
        
        Args:
            keys: List of text keys
            category: Text category
            
        Returns:
            Dictionary of key-text pairs
        """
        result = {}
        for key in keys:
            result[key] = self.get_text_by_category(category, key)
        return result
    
    def find_key_by_text(self, text: str, category: str = None) -> Optional[str]:
        """
        Find key by text value (reverse lookup)
        
        Args:
            text: Text to search for
            category: Specific category to search in (optional)
            
        Returns:
            Key if found, None otherwise
        """
        current_data = self.language_data.get(self.current_language, {})
        
        categories_to_search = [category] if category else current_data.keys()
        
        for cat in categories_to_search:
            category_data = current_data.get(cat, {})
            for key, value in category_data.items():
                if value.lower() == text.lower():
                    return key
        
        return None
    
    def validate_language_completeness(self, reference_language: str = 'en') -> Dict[str, Dict[str, List[str]]]:
        """
        Validate language completeness against reference language
        
        Args:
            reference_language: Language to use as reference
            
        Returns:
            Dictionary of missing keys per language and category
        """
        reference_lang = self._normalize_language_code(reference_language)
        reference_data = self.language_data.get(reference_lang, {})
        
        validation_result = {}
        
        for lang_code in self.get_supported_languages():
            if lang_code == reference_lang:
                continue
                
            lang_data = self.language_data.get(lang_code, {})
            missing_keys = {}
            
            for category, ref_texts in reference_data.items():
                lang_texts = lang_data.get(category, {})
                missing = [key for key in ref_texts.keys() if key not in lang_texts]
                if missing:
                    missing_keys[category] = missing
            
            validation_result[lang_code] = missing_keys
        
        return validation_result
    
    @contextmanager
    def switch_language_temporarily(self, language: str):
        """
        Context manager for temporary language switching
        
        Args:
            language: Temporary language
        """
        original_language = self.current_language
        try:
            self.set_language(language)
            yield
        finally:
            self.current_language = original_language
    
    def get_texts_for_language(self, language: str) -> Dict[str, Dict[str, str]]:
        """
        Get all texts for a specific language
        
        Args:
            language: Language code
            
        Returns:
            All texts organized by category
        """
        normalized_lang = self._normalize_language_code(language)
        return self.language_data.get(normalized_lang, {})
    
    def export_language_data(self, language: str = None) -> Dict[str, Any]:
        """
        Export language data for external use
        
        Args:
            language: Specific language to export (optional)
            
        Returns:
            Language data
        """
        if language:
            normalized_lang = self._normalize_language_code(language)
            return {
                'language': normalized_lang,
                'data': self.language_data.get(normalized_lang, {})
            }
        else:
            return {
                'current_language': self.current_language,
                'supported_languages': self.get_supported_languages(),
                'all_data': self.language_data
            }
    
    def get_available_keys(self, category: str = None, language: str = None) -> Set[str]:
        """
        Get available keys for a category and language
        
        Args:
            category: Specific category (optional)
            language: Specific language (optional)
            
        Returns:
            Set of available keys
        """
        target_lang = self._normalize_language_code(language) if language else self.current_language
        lang_data = self.language_data.get(target_lang, {})
        
        if category:
            return set(lang_data.get(category, {}).keys())
        else:
            all_keys = set()
            for cat_data in lang_data.values():
                if isinstance(cat_data, dict):
                    all_keys.update(cat_data.keys())
            return all_keys
