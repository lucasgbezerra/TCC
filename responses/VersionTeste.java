
package org.zaproxy.zap;

import org.hamcrest.MatcherAssert;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.Test;

public class VersionTest {

    @Test
    public void testEqualsSameObject() {
        Version version = new Version("1.2.3");
        MatcherAssert.assertThat(version.equals(version), Matchers.is(true));
    }

    @Test
    public void testEqualsNull() {
        Version version = new Version("1.2.3");
        MatcherAssert.assertThat(version.equals(null), Matchers.is(false));
    }

    @Test
    public void testEqualsDifferentClass() {
        Version version = new Version("1.2.3");
        MatcherAssert.assertThat(version.equals(new Object()), Matchers.is(false));
    }

    @Test
    public void testEqualsSameValues() {
        Version version1 = new Version("1.2.3");
        Version version2 = new Version("1.2.3");
        MatcherAssert.assertThat(version1.equals(version2), Matchers.is(true));
    }

    @Test
    public void testEqualsDifferentValues() {
        Version version1 = new Version("1.2.3");
        Version version2 = new Version("2.0.0");
        MatcherAssert.assertThat(version1.equals(version2), Matchers.is(false));
    }

    @Test
    public void testCompareToNull() {
        Version version = new Version("1.2.3");
        MatcherAssert.assertThat(version.compareTo(null), Matchers.is(1));
    }

    @Test
    public void testCompareToLessThan() {
        Version version1 = new Version("1.0.0");
        Version version2 = new Version("1.2.3");
        MatcherAssert.assertThat(version1.compareTo(version2), Matchers.lessThan(0));
    }

    @Test
    public void testCompareToGreaterThan() {
        Version version1 = new Version("2.0.0");
        Version version2 = new Version("1.2.3");
        MatcherAssert.assertThat(version1.compareTo(version2), Matchers.greaterThan(0));
    }

    @Test
    public void testMatchesValidRange() {
        Version version = new Version("1.2.3");
        MatcherAssert.assertThat(version.matches("1.x"), Matchers.is(true));
    }

    @Test
    public void testMatchesInvalidRange() {
        Version version = new Version("1.2.3");
        MatcherAssert.assertThat(version.matches("invalid"), Matchers.is(false));
    }

    @Test
    public void testToString() {
        Version version = new Version("1.2.3");
        MatcherAssert.assertThat(version.toString(), Matchers.is("1.2.3"));
    }
}
