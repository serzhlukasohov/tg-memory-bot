# Startup Context
_Last updated: 2024-12-19 14:30 UTC_

## What we're building
Plyn is an AI-powered mobile keyboard with voice dictation for Polish, Ukrainian, Russian, and Belarusian language speakers in Poland. The product combines voice-to-text transcription with AI text enhancement ("beautification") and translation capabilities, positioning as a voice-first alternative to Grammarly. The keyboard supports real-time voice input with superior translation quality compared to Google Translate, targeting emigrant communities who need multi-language support. Belarusian language support serves as a unique differentiator since no other mobile keyboards currently support it. The product runs on Gemini 2.5 Flash API with cloud-based processing, prioritizing speed to market over on-device privacy. Unit economics show €5/month can support ~4 hours of usage with viable margins (April 2026 costs: €0.53).

## Current Status
**Phase:** Early product development with closed TestFlight testing

**Recent Progress:**
- Translation functionality fixed and working well
- UI polished with haptic and audio feedback on paste/insert actions
- Polish language support added alongside Russian
- Product is visually impressive and team is personally excited to use it

**Critical Blockers:**
- Authentication system not yet implemented (blocking further progress)
- Firebase access granted but versioning/rollback capabilities for system prompts unclear
- Performance issues with gemini-2.5-flash model (slowdown investigation needed)

**Go-to-Market Strategy:**
- Lean validation approach: fake door landing page (plyn.io) to collect emails before full build
- Target launch: 2-3 weeks for landing page
- Market opportunity: Grammarly only added Polish support March 2026, no competitors actively marketing in Polish

## Key Decisions Made
1. **Market positioning:** Target Polish, Ukrainian, Russian, and Belarusian speakers in Poland (vs. competing in saturated English desktop market)
2. **Product strategy:** Voice-first AI keyboard with beautification layer (vs. general voice-to-text or developer tools)
3. **Validation approach:** Fake door landing page on plyn.io to test demand before building
4. **Competitive positioning:** "Better Grammarly" for voice-first + multi-language use cases
5. **Technology stack:** Gemini 2.5 Flash for processing, cloud-based MVP (vs. on-device processing)
6. **Branding:** Green color from holas.ai for beta version
7. **Language support:** Polish, Russian, Ukrainian, Belarusian with translation between them
8. **UX enhancements:** Sound effects and haptic feedback on paste/insert actions
9. **Distribution:** TestFlight for closed beta, invitation code-based access control
10. **Team tools:** GitBook for documentation/knowledge base, AI agent in chat to track decisions

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in Polish market and are they actively advertising?
- What price point do Polish/Ukrainian/Belarusian users in Poland pay for subscription products?
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on waitlist landing page?
- Is there any blocker preventing competitors from entering Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, Russian markets?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics on typical user monthly usage patterns?

**Product & Technical:**
- How to record demo video - with hands or just screencast?
- Which AI model performs best for Polish language?
- Can we access conversation context from within custom keyboard on mobile?
- How popular are voice messages and what's demand for voice-to-text in messengers?
- Can on-device models like Gemini's local version work for non-English languages?
- Why does language detection/switching work inconsistently?
- Is current model the same as previously used?
- Why is the system running slowly?
- Can GitBook's free tier support team requirements?

**Unit Economics:**
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens/minute or 30 tokens/minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?

**Use Cases:**
- Can we find underserved niche (e.g., emigrants who don't know local language)?
- What are 3-5 killer features for emigrants who don't speak Polish well?

## Next Actions

**Critical Path (Authentication & Stability):**
- Implement authentication system (currently blocking progress)
- Investigate and fix performance slowdown with gemini-2.5-flash model
- Clarify Firebase versioning/rollback capabilities for system prompts

**Landing Page Launch (2-3 week sprint):**
- Complete landing page design and development on plyn-site.vercel.app
- Set up email collection worker for waitlist
- Record real demo video on actual device showing keyboard in action
- Buy plyn.pl domain (research GoDaddy broker acquisition ~$70)
- Find Polish native speaker to verify localization

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard queries to confirm lack of competition
- Research pricing - what target users typically pay for subscription products
- Research where to find target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Ask friend launching text-to-speech startup about market insights

**Product Development:**
- Debug system prompt to fix inconsistent language detection behavior
- Test which AI model performs best for Polish language generation
- Rebuild/redraw APK after adding Polish language
- Investigate technical feasibility of accessing conversation context from custom keyboard
- Analyze voice message usage patterns in WhatsApp, Telegram, other messengers

**Competitive Analysis:**
- Perform competitor analysis of Wispr Flow, VoiceInk, others (value props, features, marketing, pricing)
- Review competitor subscription limits and pricing tiers
- Research which competitors actually support and target Polish, Ukrainian, Russian markets
- Test Whisper v3 and Gemini model performance with target languages

**Business Planning:**
- Build financial model and unit economics
- Calculate cost per hour of text based on token usage, verify counting methodology
- Find open analytics on typical user monthly usage patterns
- Create schematic launch plan to review together
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Schedule sync call to create timeline and roadmap

**Team Setup:**
- Evaluate GitBook free tier capabilities
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits