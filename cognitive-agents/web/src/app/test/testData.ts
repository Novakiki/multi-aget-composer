import type { Pattern } from '@/types';

export const TEST_PATTERNS = {
    main: {
        id: "pattern-1",
        content: "Learning happens through natural connections",
        themes: ["learning", "connections", "natural"],
        confidence: 0.85,
        evolution: {
            stage: "developing",
            history: [{
                stage: "initial",
                timestamp: "2024-01-01T00:00:00.000Z",
                changes: [{
                    type: "creation" as const,
                    description: "Pattern discovered"
                }]
            }]
        },
        connections: []
    } as Pattern,
    related: [
        {
            id: "pattern-2",
            content: "Understanding deepens over time",
            themes: ["understanding", "time", "depth"],
            confidence: 0.75,
            // ... similar structure
        },
        {
            id: "pattern-3",
            content: "Patterns connect naturally",
            themes: ["patterns", "natural", "connections"],
            confidence: 0.65,
            // ... similar structure
        }
    ]
}; 