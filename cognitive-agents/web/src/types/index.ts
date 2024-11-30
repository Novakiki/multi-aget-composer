export type ChangeType = 'creation' | 'modification' | 'connection' | 'evolution';

export interface Change {
    type: ChangeType;
    description: string;
    before?: unknown;
    after?: unknown;
}

export interface Connection {
    connectionId: string;  // Changed from id to connectionId
    type: string;
    strength: number;
    targetId: string;     // Changed from target to targetId
    description: string;
}

export interface Pattern {
    id: string;
    content: string;
    themes: string[];
    confidence: number;
    evolution: {
        stage: string;
        history: Array<{
            stage: string;
            timestamp: string;
            changes: Change[];
        }>;
    };
    connections: Connection[];
}

export class PatternError extends Error {
    constructor(message: string, public code: string) {
        super(message);
        this.name = 'PatternError';
    }
}