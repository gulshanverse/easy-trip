---
title: "MVP Scope Definition"
category: "Product"
status: "Draft"
priority: "High"
owner: "Unassigned"
last_updated: "2026-07-05"
---

# MVP Scope Definition

> **Status:** Draft
> **Purpose:** Explicit in/out feature list for the minimum viable product release.

## Guiding Principle

Ship the smallest version of the whole-trip loop — conversational planning → provider search → booking → post-booking tracking — end to end, with one provider integration per category, rather than many providers with a partial loop.

## In Scope (MVP)

### Core User-Facing Features
- Conversational trip planning (single Planner Agent): free-text input for destination(s) or "surprise me within budget", dates, traveler count, budget ceiling.
- Itinerary generation: flight + hotel combination proposals within budget, ranked by fit (not just price).
- Single-tap booking flow for the proposed itinerary (flights + hotel), with one payment provider integration.
- Post-booking dashboard: itinerary summary, booking confirmations, basic trip timeline.
- Budget Agent: running total of trip spend vs. stated budget, shown in the dashboard.
- Notification Agent (minimal): booking confirmation, flight status change alerts (delay/cancellation) via email.

### Provider Integrations (MVP — one per category)
- **Flights:** one aggregator API (e.g., a GDS-backed provider) behind the abstraction layer.
- **Hotels:** one hotel supply API behind the abstraction layer.
- **Payments:** one payment gateway (e.g., Stripe) supporting cards.
- **Maps:** one maps provider for basic location display (e.g., hotel location, points of interest referenced in itinerary).

### Platform
- Web application (responsive), no native mobile app in MVP.
- User authentication (email + OAuth), basic profile (saved travelers, payment methods).

## Explicitly Out of Scope (MVP)

- Bus and rail provider integrations (documented architecture supports them; not implemented in MVP — see `06-architecture/integration-architecture.md`).
- Local Guide Agent (in-trip recommendations) — deferred to Phase 2.
- Safety Agent (travel advisories, real-time risk alerts) — deferred to Phase 2, given the need for a reliable data source to be selected first.
- Memory Agent (long-term personalization across trips) — deferred; MVP treats each trip planning session independently.
- Multi-traveler / group trip coordination.
- Native mobile apps.
- Multi-currency support beyond one primary currency (documented as a fast-follow).
- Loyalty program integrations.
- SMS/push notifications (email only in MVP).

## Success Criteria for MVP

- A user can go from a natural-language trip request to a confirmed flight + hotel booking without leaving the platform.
- Budget Agent accurately reflects real cost against the user's stated budget at every step.
- Booking failure and provider-error states are handled gracefully (no silent failures, no double-booking risk).

## Dependencies

- Provider abstraction layer must support at least the flight, hotel, payment, and maps categories before MVP feature work begins (`06-architecture/provider-abstraction-layer.md`).
- AI agent architecture must support at least Planner and Budget agents as distinct, testable components (`06-architecture/ai-agent-architecture.md`).

## Related Documents

- `03-product/product-vision.md`
- `03-product/feature-roadmap.md`
- `06-architecture/provider-abstraction-layer.md`
- `11-ai-ml/agent-catalog.md`
