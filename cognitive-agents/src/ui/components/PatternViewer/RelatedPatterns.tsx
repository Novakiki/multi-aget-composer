'use client';

import * as React from 'react';
import type { Pattern } from '@/types';

interface RelatedPatternsProps {
    theme: string;
    patterns: Pattern[];
    onPatternSelect?: (pattern: Pattern) => void;
}

export function RelatedPatterns({ theme, patterns, onPatternSelect }: RelatedPatternsProps) {
    return (
        <div className="mt-4">
            <h4 className="font-medium text-indigo-900 mb-3">Related Patterns:</h4>
            <div className="space-y-3">
                {patterns.map((pattern) => (
                    <div 
                        key={pattern.id}
                        className="p-3 border border-indigo-100 rounded-lg hover:bg-indigo-50 
                                 cursor-pointer transition-colors duration-200"
                        onClick={() => onPatternSelect?.(pattern)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' || e.key === ' ') {
                                onPatternSelect?.(pattern);
                            }
                        }}
                        role="button"
                        tabIndex={0}
                    >
                        <p className="text-sm text-indigo-800 mb-2">{pattern.content}</p>
                        <div className="flex gap-2">
                            {pattern.themes.map((t) => (
                                <span 
                                    key={t}
                                    className={`px-2 py-1 text-xs rounded-full ${
                                        t === theme 
                                            ? 'bg-indigo-600 text-white' 
                                            : 'bg-indigo-100 text-indigo-700'
                                    }`}
                                >
                                    {t}
                                </span>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
} 