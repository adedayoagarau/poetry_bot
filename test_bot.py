#!/usr/bin/env python3
"""
Test the new poetry bot in preview mode.
"""

from bot import PoetryBot


def test_poetry_daily():
    """Test Poetry Daily extraction"""
    print("🧪 Testing Poetry Daily Source\n")

    from sources import PoetryDailySource
    from validators import ContentValidator

    source = PoetryDailySource()
    validator = ContentValidator()

    # Get today's poem
    print(f"📍 Fetching from {source.base_url}")
    poem = source.get_daily_poem()

    if not poem:
        print("❌ Failed to extract poem")
        return False

    print(f"\n✅ Extracted poem:")
    print(f"   Title: {poem.title}")
    print(f"   Author: {poem.author}")
    print(f"   Lines: {poem.line_count()}")
    print(f"   Words: {poem.word_count()}")
    print(f"   URL: {poem.source_url}")

    # Validate
    print(f"\n🔍 Validating...")
    validation = validator.validate_with_details(poem)

    print(f"   Valid: {validation['is_valid']}")
    print(f"   Reason: {validation['reason']}")
    print(f"   Word count: {validation['word_count']}")
    print(f"   Line count: {validation['line_count']}")
    print(f"   Avg line length: {validation['avg_line_length']:.1f}")

    # Show first few lines
    lines = [line.strip() for line in poem.text.split('\n') if line.strip()]
    print(f"\n📝 First 6 lines:")
    for i, line in enumerate(lines[:6], 1):
        print(f"   {i}. {line}")

    return validation['is_valid']


def test_full_bot():
    """Test full bot workflow"""
    print("\n" + "=" * 60)
    print("🧪 Testing Full Bot Workflow")
    print("=" * 60 + "\n")

    bot = PoetryBot(preview_mode=True)
    success = bot.run()

    return success


def main():
    print("🧪 " * 20)
    print("POETRY BOT TEST SUITE")
    print("🧪 " * 20 + "\n")

    # Test 1: Poetry Daily source
    test1_passed = test_poetry_daily()

    # Test 2: Full bot workflow
    test2_passed = test_full_bot()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Poetry Daily extraction: {'PASS' if test1_passed else 'FAIL'}")
    print(f"✅ Full bot workflow: {'PASS' if test2_passed else 'FAIL'}")

    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Bot is ready to use.")
        print("\n💡 Next steps:")
        print("   1. Review the preview output above")
        print("   2. Verify the poem and tweet format look good")
        print("   3. Run 'python bot.py --live' to post for real")
    else:
        print("\n❌ Some tests failed. Check output above.")

    return test1_passed and test2_passed


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
