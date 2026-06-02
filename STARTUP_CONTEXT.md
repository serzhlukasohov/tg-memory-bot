# Startup Context
_Last updated: 2024-01-09 14:30 UTC_

## What we're building
Plyn is an AI-powered voice-to-text keyboard with language beautification, targeting Polish, Ukrainian, Russian, and Belarusian speakers in Poland. The product differentiates from competitors by combining voice transcription with AI enhancement of spoken input, positioning as a "better Grammarly" alternative with voice-first input and multi-language support for emigrant communities. Using cloud-based architecture (Gemini API), the product targets non-technical mobile users who need smart text input for messaging and everyday communication. Belarusian language support serves as a potential viral hook, as no existing mobile keyboards currently support it.

## Current Status
**Phase:** Pre-launch validation  
**Immediate Priority:** Launch fake door landing page within 2-3 weeks to test market demand before building full product  
**Market Opportunity:** Clear gap identified - Grammarly only added Polish support March 2026, no competitors actively marketing in Polish  
**Unit Economics:** €5/month supports ~4 hours usage with viable margins (€0.53 current monthly costs)  
**Infrastructure:** Exploring GitBook for team documentation/knowledge sharing (Serzh evaluating free tier)

## Key Decisions Made
1. **Market Pivot:** Target Polish/Ukrainian/Belarusian speakers in Poland vs. saturated English desktop market
2. **Product Focus:** Mobile-first AI beautification keyboard vs. general voice-to-text or developer tools
3. **Technical Approach:** Cloud-based MVP using Gemini 2.5 Flash, defer on-device privacy features
4. **User Segment:** Non-technical users prioritizing convenience over privacy
5. **Go-to-Market:** Fake door landing page at plyn.io to validate demand before building
6. **Positioning:** "Better Grammarly" with voice-first and multi-language emigrant support
7. **Speed Strategy:** 2-3 week sprint to launch landing page before competitors enter
8. **Branding:** Green color from holas.ai for beta
9. **Differentiation Hook:** Belarusian language support (unsupported by existing keyboards)
10. **Team Infrastructure:** AI-first operation with shared knowledge base and agent tracking

## Open Questions
**Market & Competition:**
- What is Grammarly's actual penetration and advertising activity in Polish market?
- What price points do Polish/Ukrainian/Belarusian users in Poland pay for subscriptions?
- Is there any blocker preventing competitors from entering Polish market?
- Do existing voice-to-text solutions actively target Polish/Ukrainian/Russian markets?
- What usage limits do competitors have on subscription plans?

**Product & Technical:**
- Which AI model performs best for Polish language (Google/Gemini likely)?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- Is it technically possible to access conversation context from within custom keyboard on mobile?
- Can on-device models like Gemini work effectively for non-English languages?
- Which models (Whisper v3, Gemini) perform best with Polish and target languages?

**User Research:**
- Is there open analytics on typical monthly usage minutes users need?
- How popular are voice messages in different messengers and what's transcription demand?
- Can we find underserved niche (e.g., emigrants who don't know local language)?

**Go-to-Market:**
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on waitlist landing page?
- How to record demo video - with hands or just screencast?

## Next Actions
**Critical Path (2-3 week sprint):**
- Complete landing page design and development on plyn-site.vercel.app
- Set up email collection worker for landing page waitlist
- Record real demo video on actual device showing keyboard in action
- Find Polish native speaker to verify localization
- Schedule sync call to create timeline and roadmap

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard queries to confirm lack of competition
- Research pricing Polish/Ukrainian/Belarusian users typically pay for subscriptions
- Perform competitor analysis of Wispr Flow, VoiceInk, others (value props, features, marketing, pricing)
- Review competitor subscription limits and pricing tiers
- Research which competitors actually support and target Polish/Ukrainian/Russian markets
- Ask friend launching text-to-speech startup about market insights

**Product Development:**
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Analyze voice message usage patterns and demand for transcription in WhatsApp/Telegram

**Business & Operations:**
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Create schematic launch plan to review together in next call
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Evaluate GitBook free tier for team documentation (Serzh owns)

**Community & Distribution:**
- Research where to find target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)

**Learning:**
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits