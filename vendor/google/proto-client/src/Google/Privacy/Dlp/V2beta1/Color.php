<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/privacy/dlp/v2beta1/dlp.proto

namespace Google\Privacy\Dlp\V2beta1;

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * Represents a color in the RGB color space.
 *
 * Generated from protobuf message <code>google.privacy.dlp.v2beta1.Color</code>
 */
class Color extends \Google\Protobuf\Internal\Message
{
    /**
     * The amount of red in the color as a value in the interval [0, 1].
     *
     * Generated from protobuf field <code>float red = 1;</code>
     */
    private $red = 0.0;
    /**
     * The amount of green in the color as a value in the interval [0, 1].
     *
     * Generated from protobuf field <code>float green = 2;</code>
     */
    private $green = 0.0;
    /**
     * The amount of blue in the color as a value in the interval [0, 1].
     *
     * Generated from protobuf field <code>float blue = 3;</code>
     */
    private $blue = 0.0;

    public function __construct() {
        \GPBMetadata\Google\Privacy\Dlp\V2Beta1\Dlp::initOnce();
        parent::__construct();
    }

    /**
     * The amount of red in the color as a value in the interval [0, 1].
     *
     * Generated from protobuf field <code>float red = 1;</code>
     * @return float
     */
    public function getRed()
    {
        return $this->red;
    }

    /**
     * The amount of red in the color as a value in the interval [0, 1].
     *
     * Generated from protobuf field <code>float red = 1;</code>
     * @param float $var
     * @return $this
     */
    public function setRed($var)
    {
        GPBUtil::checkFloat($var);
        $this->red = $var;

        return $this;
    }

    /**
     * The amount of green in the color as a value in the interval [0, 1].
     *
     * Generated from protobuf field <code>float green = 2;</code>
     * @return float
     */
    public function getGreen()
    {
        return $this->green;
    }

    /**
     * The amount of green in the color as a value in the interval [0, 1].
     *
     * Generated from protobuf field <code>float green = 2;</code>
     * @param float $var
     * @return $this
     */
    public function setGreen($var)
    {
        GPBUtil::checkFloat($var);
        $this->green = $var;

        return $this;
    }

    /**
     * The amount of blue in the color as a value in the interval [0, 1].
     *
     * Generated from protobuf field <code>float blue = 3;</code>
     * @return float
     */
    public function getBlue()
    {
        return $this->blue;
    }

    /**
     * The amount of blue in the color as a value in the interval [0, 1].
     *
     * Generated from protobuf field <code>float blue = 3;</code>
     * @param float $var
     * @return $this
     */
    public function setBlue($var)
    {
        GPBUtil::checkFloat($var);
        $this->blue = $var;

        return $this;
    }

}

