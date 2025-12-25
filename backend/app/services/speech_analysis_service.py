"""
Speech Analysis Service
Real-time speech pattern analysis for linguistic markers of cognitive decline
"""

import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger
import re


class SpeechAnalysisService:
    """
    Analyzes speech patterns to detect early signs of cognitive decline

    Markers:
    - Speech rate and pauses
    - Word-finding difficulty
    - Semantic coherence
    - Vocabulary complexity
    - Repetition patterns
    - Filler words usage
    """

    def __init__(self):
        self.baseline_wpm = 150  # Normal words per minute
        self.max_pause_duration = 2.0  # seconds

        # Common filler words
        self.filler_words = {
            'um', 'uh', 'er', 'ah', 'like', 'you know', 'i mean',
            'basically', 'actually', 'literally', 'well', 'so'
        }

    def analyze_speech_recording(
        self,
        transcript: str,
        audio_duration: float,
        pause_timestamps: Optional[List[tuple]] = None,
        word_timestamps: Optional[List[tuple]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive speech analysis from transcript and timing data

        Args:
            transcript: Speech transcript text
            audio_duration: Total duration in seconds
            pause_timestamps: List of (start, end) tuples for pauses
            word_timestamps: List of (word, start, end) tuples

        Returns:
            Dictionary with speech analysis metrics
        """
        try:
            # Basic metrics
            words = transcript.lower().split()
            word_count = len(words)

            # Speech rate
            speech_rate = (word_count / audio_duration) * 60 if audio_duration > 0 else 0

            # Pause analysis
            pause_metrics = self._analyze_pauses(pause_timestamps, audio_duration)

            # Word-finding difficulty
            word_finding_metrics = self._detect_word_finding_difficulty(
                transcript, words, word_timestamps
            )

            # Semantic coherence
            coherence_score = self._calculate_semantic_coherence(transcript)

            # Vocabulary complexity
            vocab_metrics = self._analyze_vocabulary(words)

            # Repetition patterns
            repetition_metrics = self._detect_repetitions(words)

            # Filler words
            filler_metrics = self._count_filler_words(words, word_count)

            # Overall cognitive score (0-100)
            cognitive_score = self._calculate_cognitive_score({
                'speech_rate': speech_rate,
                'pause_ratio': pause_metrics['pause_ratio'],
                'word_finding_score': word_finding_metrics['difficulty_score'],
                'coherence': coherence_score,
                'vocabulary_diversity': vocab_metrics['type_token_ratio'],
                'repetition_rate': repetition_metrics['repetition_rate'],
                'filler_ratio': filler_metrics['filler_ratio']
            })

            # Risk assessment
            risk_level = self._assess_risk_level(cognitive_score)

            return {
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": audio_duration,
                "word_count": word_count,
                "speech_metrics": {
                    "speech_rate_wpm": speech_rate,
                    "baseline_deviation": abs(speech_rate - self.baseline_wpm) / self.baseline_wpm,
                    "pauses": pause_metrics,
                    "word_finding": word_finding_metrics,
                    "semantic_coherence": coherence_score,
                    "vocabulary": vocab_metrics,
                    "repetitions": repetition_metrics,
                    "fillers": filler_metrics
                },
                "cognitive_score": cognitive_score,
                "risk_level": risk_level,
                "recommendations": self._generate_recommendations(cognitive_score, risk_level)
            }

        except Exception as e:
            logger.error(f"Error analyzing speech: {e}")
            raise

    def _analyze_pauses(
        self,
        pause_timestamps: Optional[List[tuple]],
        total_duration: float
    ) -> Dict[str, Any]:
        """Analyze pause patterns"""
        if not pause_timestamps:
            return {
                "pause_count": 0,
                "total_pause_duration": 0.0,
                "average_pause_duration": 0.0,
                "pause_ratio": 0.0,
                "long_pause_count": 0
            }

        pause_durations = [end - start for start, end in pause_timestamps]
        total_pause_time = sum(pause_durations)

        long_pauses = [d for d in pause_durations if d > self.max_pause_duration]

        return {
            "pause_count": len(pause_timestamps),
            "total_pause_duration": total_pause_time,
            "average_pause_duration": np.mean(pause_durations) if pause_durations else 0,
            "pause_ratio": total_pause_time / total_duration if total_duration > 0 else 0,
            "long_pause_count": len(long_pauses),
            "max_pause_duration": max(pause_durations) if pause_durations else 0
        }

    def _detect_word_finding_difficulty(
        self,
        transcript: str,
        words: List[str],
        word_timestamps: Optional[List[tuple]] = None
    ) -> Dict[str, Any]:
        """Detect word-finding difficulties"""
        # Markers: hesitations, false starts, circumlocution
        hesitation_patterns = [
            r'\b(um+|uh+|er+|ah+)\b',
            r'\b(what\'s|what is|the thing|you know|like)\b',
            r'\b\w+\.\.\.',  # Trailing off
            r'\b(\w+)-\1\b',  # Stuttering
        ]

        hesitation_count = 0
        for pattern in hesitation_patterns:
            hesitation_count += len(re.findall(pattern, transcript.lower()))

        # False starts (words cut off mid-sentence)
        false_starts = len(re.findall(r'\b\w+-\s', transcript))

        # Calculate difficulty score
        word_count = len(words)
        difficulty_score = (hesitation_count + false_starts) / word_count if word_count > 0 else 0

        return {
            "hesitation_count": hesitation_count,
            "false_starts": false_starts,
            "difficulty_score": min(difficulty_score, 1.0),
            "severity": "high" if difficulty_score > 0.15 else "moderate" if difficulty_score > 0.08 else "low"
        }

    def _calculate_semantic_coherence(self, transcript: str) -> float:
        """
        Calculate semantic coherence score
        Simple heuristic based on sentence structure and topic consistency
        """
        sentences = re.split(r'[.!?]+', transcript)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 2:
            return 1.0

        # Check for sentence completeness
        complete_sentences = sum(1 for s in sentences if len(s.split()) >= 4)
        completeness_ratio = complete_sentences / len(sentences)

        # Check for topic jumps (simplified: look for connecting words)
        connectors = ['and', 'but', 'so', 'then', 'therefore', 'however', 'because']
        connector_count = sum(1 for s in sentences for word in connectors if word in s.lower())

        # Coherence score (0-1)
        coherence = (completeness_ratio * 0.7) + (min(connector_count / len(sentences), 1.0) * 0.3)

        return coherence

    def _analyze_vocabulary(self, words: List[str]) -> Dict[str, Any]:
        """Analyze vocabulary complexity and diversity"""
        if not words:
            return {
                "unique_words": 0,
                "type_token_ratio": 0,
                "average_word_length": 0,
                "complexity_score": 0
            }

        # Remove filler words for accurate vocabulary assessment
        content_words = [w for w in words if w not in self.filler_words]

        unique_words = set(content_words)

        # Type-token ratio (vocabulary diversity)
        ttr = len(unique_words) / len(content_words) if content_words else 0

        # Average word length (proxy for complexity)
        avg_length = np.mean([len(w) for w in content_words]) if content_words else 0

        # Complexity score
        complexity = (ttr * 0.6) + (min(avg_length / 10, 1.0) * 0.4)

        return {
            "total_words": len(words),
            "content_words": len(content_words),
            "unique_words": len(unique_words),
            "type_token_ratio": ttr,
            "average_word_length": avg_length,
            "complexity_score": complexity
        }

    def _detect_repetitions(self, words: List[str]) -> Dict[str, Any]:
        """Detect word and phrase repetitions"""
        if not words:
            return {
                "word_repetitions": 0,
                "phrase_repetitions": 0,
                "repetition_rate": 0
            }

        # Word repetitions
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

        # Count excessive repetitions (same word used >5% of total)
        threshold = len(words) * 0.05
        excessive_reps = sum(1 for count in word_counts.values() if count > threshold)

        # Phrase repetitions (2-3 word sequences)
        phrase_counts = {}
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

        phrase_reps = sum(1 for count in phrase_counts.values() if count > 1)

        repetition_rate = (excessive_reps + phrase_reps) / len(words)

        return {
            "word_repetitions": excessive_reps,
            "phrase_repetitions": phrase_reps,
            "repetition_rate": repetition_rate,
            "severity": "high" if repetition_rate > 0.10 else "moderate" if repetition_rate > 0.05 else "low"
        }

    def _count_filler_words(self, words: List[str], total_words: int) -> Dict[str, Any]:
        """Count filler word usage"""
        filler_count = sum(1 for word in words if word in self.filler_words)
        filler_ratio = filler_count / total_words if total_words > 0 else 0

        return {
            "filler_count": filler_count,
            "filler_ratio": filler_ratio,
            "severity": "high" if filler_ratio > 0.15 else "moderate" if filler_ratio > 0.08 else "low"
        }

    def _calculate_cognitive_score(self, metrics: Dict[str, float]) -> float:
        """
        Calculate overall cognitive score (0-100)
        Higher score = better cognitive function
        """
        # Normalize each metric (0-1, where 1 is healthy)

        # Speech rate (penalize deviation from normal)
        rate_score = 1.0 - min(metrics.get('speech_rate', 150) / 200, 1.0)

        # Pauses (lower is better)
        pause_score = 1.0 - min(metrics.get('pause_ratio', 0) * 5, 1.0)

        # Word finding (lower difficulty is better)
        wf_score = 1.0 - min(metrics.get('word_finding_score', 0) * 3, 1.0)

        # Coherence (higher is better)
        coherence_score = metrics.get('coherence', 1.0)

        # Vocabulary diversity (higher is better)
        vocab_score = metrics.get('vocabulary_diversity', 0.5)

        # Repetitions (lower is better)
        rep_score = 1.0 - min(metrics.get('repetition_rate', 0) * 10, 1.0)

        # Fillers (lower is better)
        filler_score = 1.0 - min(metrics.get('filler_ratio', 0) * 5, 1.0)

        # Weighted average
        overall_score = (
            rate_score * 0.15 +
            pause_score * 0.20 +
            wf_score * 0.25 +
            coherence_score * 0.15 +
            vocab_score * 0.10 +
            rep_score * 0.10 +
            filler_score * 0.05
        )

        return overall_score * 100

    def _assess_risk_level(self, cognitive_score: float) -> str:
        """Assess cognitive decline risk based on score"""
        if cognitive_score >= 80:
            return "low"
        elif cognitive_score >= 65:
            return "moderate"
        elif cognitive_score >= 50:
            return "high"
        else:
            return "very_high"

    def _generate_recommendations(self, score: float, risk_level: str) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []

        if risk_level in ["high", "very_high"]:
            recommendations.append("Consider comprehensive cognitive evaluation by a specialist")
            recommendations.append("Schedule follow-up speech analysis in 1-2 weeks")

        if score < 70:
            recommendations.append("Practice word-finding exercises and vocabulary games")
            recommendations.append("Engage in regular conversation with family and friends")

        if score < 80:
            recommendations.append("Monitor speech patterns during future assessments")

        if not recommendations:
            recommendations.append("Continue regular cognitive monitoring")

        return recommendations


# Singleton instance
speech_analysis_service = SpeechAnalysisService()
