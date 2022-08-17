from django.test import SimpleTestCase

from website.common.streamfield import (
    IGNORE_HEADING_BLOCKS,
    IGNORE_PLAINTEXT_BLOCKS,
    get_blocks,
)


class StreamFieldBlocksTestCase(SimpleTestCase):
    def test_ignored_plaintext_blocks(self) -> None:
        plaintext_block_classes = [c[1].__class__ for c in get_blocks()]

        for block_class in IGNORE_PLAINTEXT_BLOCKS:
            self.assertIn(block_class, plaintext_block_classes)

    def test_ignored_heading_blocks(self) -> None:
        heading_block_classes = [c[1].__class__ for c in get_blocks()]

        for block_class in IGNORE_HEADING_BLOCKS:
            self.assertIn(block_class, heading_block_classes)
