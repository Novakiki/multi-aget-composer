'use client';

import React, { useState } from 'react';
import type { Pattern, Insight } from '@/types/components';

interface InteractionSpaceProps {
    onQuestionSubmit?: (question: string) => void;
    onPatternExplore?: (pattern: Pattern) => void;
    onInsightCapture?: (insight: Insight) => void;
}

export function InteractionSpace({ 
    onQuestionSubmit,
    onPatternExplore,
    onInsightCapture 
}: InteractionSpaceProps) {
    const [question, setQuestion] = useState('');

    return (
        <div className="p-4 border rounded-lg shadow-sm">
            <h2 className="text-lg font-semibold mb-4">Interaction Space</h2>
            <div className="space-y-4">
                {/* Question Input */}
                <div>
                    <label htmlFor="question" className="block text-sm font-medium mb-2">
                        Ask a Question
                    </label>
                    <input 
                        id="question"
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        className="w-full p-2 border rounded"
                        placeholder="What patterns do you notice?"
                    />
                </div>

                {/* Pattern Explorer */}
                <div>
                    <h3 className="text-md font-medium mb-2">Pattern Explorer</h3>
                    <div className="p-4 border rounded bg-gray-50">
                        Pattern exploration coming soon...
                    </div>
                </div>

                {/* Insight Capture */}
                <div>
                    <h3 className="text-md font-medium mb-2">Capture Insight</h3>
                    <div className="p-4 border rounded bg-gray-50">
                        Insight recording coming soon...
                    </div>
                </div>
            </div>
        </div>
    );
} 