"""Fit Newton's cooling law and predict when the coffee reaches 40 °C."""
import numpy as np

from plot_support import BLUE, MUTED, RUST, TEAL, figure, options, save


def temperature(t, room, initial_excess, k):
    return room + initial_excess * np.exp(-k * t)


def euler_excess(times, initial_excess, k):
    # The same differential equation becomes a state-update loop:
    # excess_next ~= excess_now + (rate_now * elapsed_time).
    path = np.empty(len(times))
    path[0] = initial_excess
    for i, dt in enumerate(np.diff(times)):
        rate = -k * path[i]
        path[i + 1] = path[i] + rate * dt
    return path


def main():
    args = options(__doc__)
    room, initial, reading, reading_time, target = 20.0, 90.0, 60.0, 10.0, 40.0
    initial_excess = initial - room
    fitted_excess = reading - room
    target_excess = target - room

    # PAPER: E'= -k*E implies E(t)=E(0)*exp(-k*t). Isolate k with the fit
    # reading, then solve the same equation for the time at the target excess.
    k = np.log(initial_excess / fitted_excess) / reading_time
    target_time = np.log(initial_excess / target_excess) / k
    assert np.isclose(temperature(reading_time, room, initial_excess, k), reading)
    assert np.isclose(temperature(target_time, room, initial_excess, k), target)
    print(f"Fitted cooling constant k: {k:.8f} per minute.")
    print(f"Model prediction: {target:.0f} °C at {target_time:.4f} minutes after the start.")
    print("The 10-minute point fits the model. The 40 °C crossing is a prediction.")

    fig, (left, right) = figure(args, "09", "Predicting how coffee cools")
    t = np.linspace(0, 40, 500)
    exact = temperature(t, room, initial_excess, k)
    left.plot(t, exact, color=TEAL, lw=2.3, label="Analytical model")
    left.plot([0, target_time, target_time], [target, target, room-2], ":", color=MUTED, lw=1.3)
    left.axhline(room, color=MUTED, ls="--", lw=1, label="Room temperature")
    left.scatter([0, reading_time], [initial, reading], color=BLUE, s=52, zorder=4,
                 label="Given readings")
    left.scatter([target_time], [target], color=RUST, marker="D", s=54, zorder=4,
                 label=f"Predicted crossing at {target_time:.1f} min")
    left.set(title="Fit a curve, then make a prediction", xlabel="Time (min)", ylabel="Coffee temperature (°C)",
             xlim=(-1, 40), ylim=(16, 95))
    left.legend(loc="upper right")

    # Compare a direct analytical solution to time-stepping the differential
    # equation. Both use the same fitted k. Neither is a new observation.
    for dt, color in [(2.0, RUST), (0.5, BLUE), (0.1, TEAL)]:
        times = np.arange(round(40 / dt) + 1) * dt
        euler = room + euler_excess(times, initial_excess, k)
        error = euler - temperature(times, room, initial_excess, k)
        right.plot(times, error, color=color, lw=2, label=f"Euler step = {dt:g} min")
        print(f"Euler step {dt:g} min -> max model difference {np.max(np.abs(error)):.4f} °C.")
    right.axhline(0, color=MUTED, lw=0.8)
    right.set(title="Smaller software steps track the model better", xlabel="Time (min)",
              ylabel="Euler temperature − analytical temperature (°C)")
    right.legend(loc="lower right")
    save(fig, args, "09_coffee_cooling")


if __name__ == "__main__":
    main()
