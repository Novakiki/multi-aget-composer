'use client';

import { useEffect, useState } from 'react';
import type { Pattern } from '@/types/components';

interface PatternViewerProps {
    pattern?: Pattern;
    onPatternSelect?: (pattern: Pattern) => void;
}

export function PatternViewer({ pattern, onPatternSelect }: PatternViewerProps) {
    const [selectedPattern, setSelectedPattern] = useState<Pattern | null>(null);

    useEffect(() => {
        if (pattern) {
            setSelectedPattern(pattern);
        }
    }, [pattern]);

    return (
        <div className="p-4 border rounded-lg shadow-sm">
            <h2 className="text-lg font-semibold mb-4">Pattern Viewer</h2>
            {selectedPattern ? (
                <div className="space-y-2">
                    <div>
                        <span className="font-medium">Content:</span>
                        <p>{selectedPattern.content}</p>
                    </div>
                    <div>
                        <span className="font-medium">Themes:</span>
                        <div className="flex gap-2">
                            {selectedPattern.themes.map((theme) => (
                                <span 
                                    key={theme}
                                    className="px-2 py-1 bg-blue-100 rounded-full text-sm"
                                >
                                    {theme}
                                </span>
                            ))}
                        </div>
                    </div>
                    <div>
                        <span className="font-medium">Confidence:</span>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                                className="bg-blue-600 h-2 rounded-full"
                                style={{ width: `${selectedPattern.confidence * 100}%` }}
                            />
                        </div>
                    </div>
                </div>
            ) : (
                <p className="text-gray-500">No pattern selected</p>
            )}
        </div>
    );
} 