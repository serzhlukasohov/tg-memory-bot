# Startup Context
_Last updated: 2026-05-15_

## What we're building
Plyn is a voice-first AI keyboard targeting Polish, Ukrainian, and Belarusian language speakers in Poland. The product combines voice-to-text transcription with an AI beautification layer that improves grammar and style. Key differentiators: voice-first input, multi-language support for emigrant communities (especially Belarusian - currently unsupported on mobile keyboards), and competitive pricing positioned against Grammarly (which only added Polish support in March 2026). The product uses Gemini API for both audio transcription and text processing.

## Current Status
**Phase:** Transitioning from technical prototype to business validation
**Immediate Priority:** Launch fake door landing page at plyn.io within 2-3 weeks to collect waitlist emails and validate demand
**Unit Economics:** €5/month supports ~4 hours usage with 100% margin minus 30% Apple commission
**Current Costs:** €0.53 (April 2026)
**Beta Strategy:** Target 100 Ukrainian/Belarusian users as underserved market segment

## Key Decisions Made
1. **Market positioning** - Target Polish/Ukrainian/Belarusian speakers in Poland as underserved segment with no active competition marketing in Polish
2. **Competitive strategy** - Position as "better Grammarly" with voice-first and multi-language focus
3. **Belarusian language support** - Use as viral GTM hook (no mobile keyboard supports it); implement via Gemini 2.5 Flash
4. **Lean validation** - Launch fake door landing page before building full product
5. **Domain** - Use plyn.io for brand
6. **Pricing model** - €5/month for ~4 hours usage; compete on low price initially
7. **Beta scope** - 100 users from Ukrainian/Belarusian communities
8. **Technology stack** - Continue using Gemini API over OpenAI Whisper for cost efficiency
9. **Branding** - Use green color from holas.ai for beta phase
10. **Optimization sequence** - Defer VAD improvements until after beta test

## Open Questions
- What is Grammarly's penetration in Polish market and are they actively advertising?
- What price points do Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products?
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on waitlist landing page?
- How to record demo video - with hands or screencast only?
- What blockers might prevent competitors from entering Polish market?
- Which AI model performs best for Polish language generation?

## Next Actions
**Landing Page & Launch:**
- Complete landing page design and development on plyn-site.vercel.app
- Set up email collection worker for waitlist
- Record real demo video on actual device
- Buy plyn.pl domain (research GoDaddy broker, ~$70)
- Find Polish native speaker to verify localization

**Market Research:**
- Research Grammarly's penetration and advertising in Polish market
- Manually verify Google search results for Polish keyboard queries
- Research typical subscription pricing for target audience
- Generate 3-5 killer features for emigrants who don't speak Polish well
- Research audience acquisition channels (Telegram groups, Facebook Warsaw/Wroclaw communities)
- Test which AI model performs best for Polish language
- Ask friend in text-to-speech startup about market insights

**Planning:**
- Build financial model and unit economics
- Schedule sync call to create timeline and roadmap for 2-3 week sprint
- Set up shared AI agent with knowledge base to track decisions
- Watch JTBD (Jobs-to-be-Done) video tutorial