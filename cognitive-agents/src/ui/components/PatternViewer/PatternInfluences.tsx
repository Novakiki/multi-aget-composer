'use client';

import * as React from 'react';
import type { Pattern } from '../../types/components';
import { PatternNetwork } from './PatternNetwork';

interface PatternInfluencesProps {
    pattern: Pattern;
}

export function PatternInfluences({ pattern }: PatternInfluencesProps) {
    const handleExploreConnection = (connectionId: string) => {
        console.log(`Exploring connection: ${connectionId}`);
        // TODO: Implement deep connection exploration
    };

    return (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-3">Pattern Relationships</h4>
            
            {/* Direct Influences */}
            <div className="space-y-4">
                <div className="p-3 bg-white rounded-lg">
                    <h5 className="text-sm font-medium text-blue-800 mb-2">
                        Direct Connections
                    </h5>
                    <div className="flex items-center gap-2">
                        <div className="flex-grow h-1 bg-blue-100 rounded-full">
                            <div className="h-1 bg-blue-500 rounded-full" 
                                 style={{ width: '75%' }} />
                        </div>
                        <span className="text-sm text-blue-600">75% overlap</span>
                    </div>
                    <p className="mt-2 text-sm text-blue-700">
                        This pattern frequently appears with themes of learning and growth
                    </p>
                </div>

                {/* Emerging Connections */}
                <div className="p-3 bg-white rounded-lg">
                    <h5 className="text-sm font-medium text-blue-800 mb-2">
                        Emerging Relationships
                    </h5>
                    <ul className="space-y-2 text-sm text-blue-700">
                        <li>• New connection forming with "natural learning"</li>
                        <li>• Growing relationship with "pattern evolution"</li>
                        <li>• Potential link to "understanding development"</li>
                    </ul>
                </div>

                {/* Questions & Uncertainties */}
                <div className="p-3 bg-white rounded-lg">
                    <h5 className="text-sm font-medium text-blue-800 mb-2">
                        Open Questions
                    </h5>
                    <ul className="space-y-2 text-sm text-blue-700">
                        <li>• Is there a stronger connection we're missing?</li>
                        <li>• How do these relationships evolve over time?</li>
                        <li>• What patterns might emerge next?</li>
                    </ul>
                </div>
            </div>

            <PatternNetwork 
                pattern={pattern}
                onExploreConnection={handleExploreConnection}
            />
        </div>
    );
} 