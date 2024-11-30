interface UnderstandingFlowProps {
    pattern: Pattern;
}

export function UnderstandingFlow({ pattern }: UnderstandingFlowProps) {
    return (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-800 mb-3">Understanding Development</h4>
            
            {/* Show how understanding grows */}
            <div className="space-y-3">
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-indigo-600 rounded-full" />
                    <span className="text-sm text-gray-600">Initial observation</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-indigo-400 rounded-full" />
                    <span className="text-sm text-gray-600">Pattern recognition</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-indigo-300 rounded-full" />
                    <span className="text-sm text-gray-600">Deeper connections</span>
                </div>
            </div>

            {/* Questions that arise */}
            <div className="mt-4">
                <h5 className="text-sm font-medium text-gray-700 mb-2">
                    Questions to Explore:
                </h5>
                <ul className="space-y-2 text-sm text-gray-600">
                    <li>• How do these patterns connect?</li>
                    <li>• What other patterns might be related?</li>
                    <li>• How does this understanding grow?</li>
                </ul>
            </div>
        </div>
    );
} 