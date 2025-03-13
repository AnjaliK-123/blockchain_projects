// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

library FixedPoint {
    // Fixed point representation with 112 bits of precision
    struct uq112x112 {
        uint224 _x; // The actual value stored as a uint224
    }

    // Convert a uint to uq112x112
    function encode(uint y) internal pure returns (uq112x112 memory) {
        return uq112x112(uint224(y) << 112);
    }

    // Convert uq112x112 to uint
    function decode(uq112x112 memory self) internal pure returns (uint) {
        return self._x >> 112;
    }

    // Multiply two uq112x112 values
    function mul(uq112x112 memory self, uint y) internal pure returns (uq112x112 memory) {
        return uq112x112((self._x * y) >> 112);
    }

    // Divide two uq112x112 values
    function div(uq112x112 memory self, uint y) internal pure returns (uq112x112 memory) {
        return uq112x112((self._x << 112) / y);
    }

    // Add two uq112x112 values
    function add(uq112x112 memory self, uq112x112 memory other) internal pure returns (uq112x112 memory) {
        return uq112x112(self._x + other._x);
    }

    // Subtract two uq112x112 values
    function sub(uq112x112 memory self, uq112x112 memory other) internal pure returns (uq112x112 memory) {
        return uq112x112(self._x - other._x);
    }
}