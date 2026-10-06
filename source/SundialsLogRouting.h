#ifndef ROADRUNNER_SUNDIALSLOGROUTING_H
#define ROADRUNNER_SUNDIALSLOGROUTING_H

#include "rrLogger.h"

#include <sundials/sundials_config.h>
#include <sundials/sundials_context.h>
#include <sundials/sundials_logger.h>

namespace rr {

    /**
     * Since SUNDIALS 7, CVODE warnings (e.g. "t + h = t") are not passed to the
     * SUNContext error handlers; they are queued on the context's SUNLogger, which
     * by default prints them to stdout. SUNDIALS 7.8.0 added
     * SUNLogger_SetQueueAndFlushMsgFns, which lets us receive them instead.
     */
#if (SUNDIALS_VERSION_MAJOR > 7) || (SUNDIALS_VERSION_MAJOR == 7 && SUNDIALS_VERSION_MINOR >= 8)
#define RR_SUNDIALS_HAS_LOGGER_CALLBACKS 1

    inline SUNErrCode sundialsLogToRRLogger(SUNLogger /*logger*/, SUNLogLevel lvl, const char* /*prefix*/,
                                            int /*rank*/, const char* /*scope*/, const char* label,
                                            const char* payload, void* /*content*/) {
        const char* text = payload ? payload : "";
        const char* function = label ? label : "";
        switch (lvl) {
            case SUN_LOGLEVEL_ERROR:
                rrLog(Logger::LOG_ERROR) << "SUNDIALS Error, Function: " << function << ", Message: " << text;
                break;
            case SUN_LOGLEVEL_WARNING:
                rrLog(Logger::LOG_WARNING) << "SUNDIALS Warning, Function: " << function << ", Message: " << text;
                break;
            case SUN_LOGLEVEL_INFO:
                rrLog(Logger::LOG_INFORMATION) << "SUNDIALS Info, Function: " << function << ", Message: " << text;
                break;
            case SUN_LOGLEVEL_DEBUG:
                rrLog(Logger::LOG_DEBUG) << "SUNDIALS Debug, Function: " << function << ", Message: " << text;
                break;
            default:
                break;
        }
        return SUN_SUCCESS;
    }

    inline SUNErrCode sundialsLogFlush(SUNLogger /*logger*/, SUNLogLevel /*lvl*/, void* /*content*/) {
        return SUN_SUCCESS;
    }
#endif

    /**
     * Make the SUNLogger of a freshly created SUNContext send its messages to the
     * RoadRunner Logger instead of stdout/stderr. The logger is the one created by
     * SUNContext_Create and is owned (and freed) by the context.
     * @return true if messages are now routed to the RoadRunner Logger. If false
     * (SUNDIALS older than 7.8.0), SUNDIALS keeps writing warnings to stdout.
     */
    inline bool routeSundialsLogToRRLogger(SUNContext sunctx) {
#ifdef RR_SUNDIALS_HAS_LOGGER_CALLBACKS
        SUNLogger logger = nullptr;
        if (SUNContext_GetLogger(sunctx, &logger) != SUN_SUCCESS || !logger) {
            return false;
        }
        return SUNLogger_SetQueueAndFlushMsgFns(logger, sundialsLogToRRLogger, sundialsLogFlush, nullptr) ==
               SUN_SUCCESS;
#else
        (void) sunctx;
        return false;
#endif
    }
}

#endif //ROADRUNNER_SUNDIALSLOGROUTING_H
