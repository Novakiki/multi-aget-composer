'use client';

import React, { useEffect, useState } from 'react';
import type { Pattern } from '@/types/components';

interface PatternViewerProps {
    pattern?: Pattern;
    onPatternSelect?: (pattern: Pattern) => void;
}

export function PatternViewer({ pattern, onPatternSelect }: PatternViewerProps) {
    const [isClient, setIsClient] = useState(false);
    const [selectedPattern, setSelectedPattern] = useState<Pattern | null>(null);

    useEffect(() => {
        setIsClient(true);
        if (pattern) {
            setSelectedPattern(pattern);
        }
    }, [pattern]);

    if (!isClient) {
        return null;
    }

    return (
        <div className="p-4 border rounded-lg shadow-sm bg-white">
            <h2 className="text-lg font-semibold mb-4 text-gray-800">Pattern Viewer</h2>
            {selectedPattern ? (
                <div className="space-y-2">
                    <div>
                        <span className="font-medium text-gray-700">Content:</span>
                        <p className="text-gray-600">{selectedPattern.content}</p>
                    </div>
                    <div>
                        <span className="font-medium text-gray-700">Themes:</span>
                        <div className="flex gap-2">
                            {selectedPattern.themes.map((theme) => (
                                <span 
                                    key={theme}
                                    className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium"
                                >
                                    {theme}
                                </span>
                            ))}
                        </div>
                    </div>
                    <div>
                        <span className="font-medium text-gray-700">Confidence:</span>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                                className="bg-indigo-600 h-2 rounded-full"
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