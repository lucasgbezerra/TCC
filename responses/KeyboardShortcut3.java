
package org.zaproxy.zap.extension.keyboard;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.is;
import org.junit.jupiter.api.Test;

public class KeyboardShortcutTest {

    @Test
    public void testKeyboardShortcutMethod() {
        KeyboardShortcut keyboardShortcut = new KeyboardShortcut();
        
        boolean result = keyboardShortcut.someMethodToTest();
        
        assertThat(result, is(true));
    }
}
