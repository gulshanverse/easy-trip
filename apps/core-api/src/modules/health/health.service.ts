import { Injectable } from '@nestjs/common';

export interface HealthStatus {
  status: 'ok';
  uptimeSeconds: number;
  timestamp: string;
  service: string;
}

@Injectable()
export class HealthService {
  private readonly startedAt = Date.now();

  getStatus(): HealthStatus {
    return {
      status: 'ok',
      uptimeSeconds: Math.floor((Date.now() - this.startedAt) / 1000),
      timestamp: new Date().toISOString(),
      service: 'core-api',
    };
  }
}
